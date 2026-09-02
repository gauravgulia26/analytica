# 📋 Analytica Architecture & Orchestration TODO

This document provides an in-depth architectural review of the current `analytica/agents` module and outlines actionable suggestions to achieve a modular, maintainable, and frictionless ("easy-going") multi-agent orchestration implementation with **LangGraph**.

---

## 🔍 1. Current Codebase Analysis & Identified Bottlenecks

After analyzing the latest additions in `analytica/agents/`, `analytica/schema/`, `analytica/prompts/`, and `main.py`, the following architectural bottlenecks were identified:

### 1.1 Eager Import-Time Execution (`analytica/agents/factory/chains.py`)
* **Current state**: `SUPERVISOR_CHAIN = load_supervisor_chain()` is executed directly at module load time.
* **Problem**: 
  - Importing `chains.py` immediately validates environment variables and initializes Groq clients.
  - If `GROQ_API_KEY` is not loaded yet (or during unit test collection in CI), the entire import fails.
  - Chains cannot be dynamically reconfigured with different models or parameters.
* **Suggestion**: Replace top-level variables with a lazy-loading factory pattern or cache function (`get_supervisor_chain()`).

### 1.2 Agent Boilerplate Duplication (`analytica/agents/supervisor/llm.py`)
* **Current state**: `GetLLM` dataclass is defined specifically for the supervisor agent inside `analytica/agents/supervisor/llm.py`.
* **Problem**: When adding the remaining 6 agents (`data_analyst`, `statistical_analyst`, `visualisation`, `critic`, `interpretation`, `report_generation`), this exact same `GetLLM` class will be copied and pasted 6 times.
* **Suggestion**: Create a generic, reusable `AgentBuilder` or `BaseAgent` in `analytica/agents/common/` that accepts `(agent_name, prompt_name, output_schema)` to generate any agent chain in 2 lines of code.

### 1.3 Context-Blind Supervisor Prompt (`analytica/agents/supervisor/chain.py`)
* **Current state**: `make_prompt_template` only passes `input_variables=["user_query"]`.
* **Problem**:
  - The comprehensive prompt in `analytica/prompts/supervisor_prompt.md` instructs the supervisor to inspect dataset structure, review outputs of previous agents, identify completed work, and replan.
  - However, the chain currently only passes `user_query`. The supervisor is completely blind to dataset schema, previous agent executions, and execution history.
* **Suggestion**: Expand the supervisor prompt input to accept `dataset_metadata`, `execution_history`, and `previous_results` formatted as structured strings.

### 1.4 Schema Indirection & Fragmentation
* **Current state**: 
  - `analytica/schema/agents_schema/supervisor_schema.py` defines `SupervisorOutput`.
  - `analytica/agents/supervisor/schema.py` imports and re-exports it through a `get_schema()` wrapper.
* **Problem**: Having redundant wrapper files across two disconnected directories (`analytica/schema/` and `analytica/agents/`) adds unnecessary file hopping and indirection.
* **Suggestion**: Standardize schema location. Either colocate schemas within each agent directory (`analytica/agents/<agent>/schemas.py`) as outlined in the project README, or centralize all agent schemas inside `analytica/schema/` without empty proxy files.

### 1.5 Missing Standardized LangGraph Node Adapters
* **Current state**: The supervisor chain outputs a Pydantic object `SupervisorOutput(next_action=..., task=...)`, but there is no standardized way to integrate this into a LangGraph node.
* **Problem**: If each agent handles LangGraph state extraction and state updating differently, orchestration code in `orchestration/nodes/` will become messy and full of repetitive glue code.
* **Suggestion**: Provide a standard `create_agent_node()` helper that automatically unpacks state, invokes the chain, and packages the return dict for LangGraph.

---

## 🚀 2. Proposed Architectural Enhancements

### 💡 Recommendation 1: Generic Agent Factory & Base Pattern

Instead of creating separate `llm.py`, `chain.py`, and `schema.py` for every single agent, implement a single generic agent factory:

```python
# Proposed: analytica/agents/common/builder.py
from typing import Type
from pydantic import BaseModel
from langchain_core.runnables import Runnable
from analytica.providers.factory import ProviderFactory
from analytica.agents.common.utils import make_prompt_template

def create_agent_chain(
    agent_name: str,
    prompt_name: str,
    output_schema: Type[BaseModel] | None = None,
    provider_name: str = "groq",
) -> Runnable:
    """
    Unified factory to build any agent chain in the Analytica system.
    """
    prompt = make_prompt_template(prompt_name)
    base_llm = ProviderFactory(provider_name=provider_name, agent_name=agent_name).get_llm()
    
    if output_schema:
        llm = base_llm.with_structured_output(schema=output_schema)
    else:
        llm = base_llm
        
    return prompt | llm
```

**Benefits**:
- Reduces code required per agent by ~80%.
- Eliminates duplicated `GetLLM` dataclasses.
- Consistent configuration and provider handling across all agents.

---

### 💡 Recommendation 2: Lazy Chain Instantiation & Registry

Replace module-level instantiation in `chains.py` with a thread-safe / memoized registry:

```python
# Proposed: analytica/agents/factory/chains.py
from functools import lru_cache
from langchain_core.runnables import Runnable
from analytica.agents.supervisor.chain import load_supervisor_chain

@lru_cache(maxsize=1)
def get_supervisor_chain() -> Runnable:
    """Lazily load and cache the supervisor chain upon first request."""
    return load_supervisor_chain()

def get_agent_chain(agent_name: str) -> Runnable:
    """Dispatch lookup for any configured agent chain."""
    registry = {
        "supervisor_agent": get_supervisor_chain,
        # "data_analyst_agent": get_data_analyst_chain,
        # ...
    }
    if agent_name not in registry:
        raise KeyError(f"No chain registered for agent: {agent_name}")
    return registry[agent_name]()
```

**Benefits**:
- Zero network or environment side-effects when importing modules.
- Fast, deterministic unit testing without requiring mock environment variables on import.

---

### 💡 Recommendation 3: Context-Rich Supervisor State Inputs

Update the supervisor chain inputs to reflect full workflow context needed for iterative decision-making:

```python
# State fields to inject into supervisor prompt:
{
    "user_query": state["user_query"],
    "dataset_metadata": format_dataset_metadata(state.get("dataset_metadata")),
    "execution_history": format_history(state.get("plan_history", [])),
    "latest_findings": format_findings(state.get("agent_results", {}))
}
```

**Supervisor Output Schema Enhancement**:
Extend `SupervisorOutput` to support both step-by-step routing and strategic tracking:
```python
class SupervisorOutput(BaseModel):
    next_action: NextAction = Field(description="Next agent to invoke or 'end'")
    task: str = Field(description="Specific instructions for the next agent")
    is_replan: bool = Field(default=False, description="True if previous step failed or required revision")
    reasoning: str = Field(description="Brief rationale for this routing decision")
```

---

### 💡 Recommendation 4: Zero-Boilerplate LangGraph Node Adapters

Create a lightweight node adapter utility that converts any agent chain into a LangGraph node function:

```python
# Proposed: analytica/orchestration/nodes/adapter.py
from typing import Callable, Any
from langchain_core.runnables import Runnable

def make_agent_node(
    chain: Runnable,
    input_key_map: dict[str, str],
    output_state_key: str,
) -> Callable[[dict[str, Any]], dict[str, Any]]:
    """
    Creates a LangGraph node function from a Runnable chain.
    
    Args:
        chain: The agent Runnable pipeline.
        input_key_map: Mapping from chain input variables to LangGraph state keys.
        output_state_key: The state key where the agent result will be saved.
    """
    def node(state: dict[str, Any]) -> dict[str, Any]:
        inputs = {param: state.get(state_key) for param, state_key in input_key_map.items()}
        result = chain.invoke(inputs)
        return {output_state_key: result}
    
    return node
```

**Benefits**:
- Keeps the `agents/` package completely free of LangGraph dependencies.
- Keeps `orchestration/nodes/` clean and declarative.

---

### 💡 Recommendation 5: 1-to-1 Node Routing Alignment

Ensure that values of the `NextAction` enum match LangGraph node names directly:

```python
class NextAction(str, Enum):
    DATA_ANALYST = "data_analyst"
    STATISTICAL_ANALYST = "statistical_analyst"
    PYTHON_ANALYSIS = "python_analysis"
    VISUALIZATION = "visualization"
    CRITIC = "critic"
    INTERPRETATION = "interpretation"
    REPORT = "report"
    END = "end"
```

In LangGraph routing edge:
```python
# routing becomes a clean 1-liner:
workflow.add_conditional_edges(
    "supervisor",
    lambda state: state["supervisor_output"].next_action.value,
    {
        "data_analyst": "data_analyst_node",
        "statistical_analyst": "statistical_analyst_node",
        "python_analysis": "python_analysis_subgraph",
        "visualization": "visualization_node",
        "critic": "critic_node",
        "interpretation": "interpretation_node",
        "report": "report_node",
        "end": END,
    }
)
```

---

### 💡 Recommendation 6: Structured Context Serializers

In `analytica/agents/common/utils.py`, add standard serializers for complex Python/Pandas data:
- `serialize_schema(df_metadata)`: Formats columns, data types, null counts, and cardinality into a clean Markdown table.
- `serialize_agent_results(results)`: Formats outputs from previous agents into bulleted summaries.
- `serialize_critic_feedback(critique)`: Highlights rejected hypotheses or needed re-analyses.

---

### 💡 Recommendation 7: Robustness & Output Fallback Handling

LLM structured output parsing can occasionally fail due to JSON truncation or provider hiccups.
Add standard retry and fallback semantics to the agent runner:
- Use `.with_retry(stop_after_attempt=3)` on the LLM chain.
- Support a fallback raw-output repair parser if Pydantic parsing fails.

---

## 📋 3. Prioritized Implementation Roadmap (TODO List)

### Phase 1: Core Clean-Up & Foundation
- [ ] **1.1 Fix Eager Import Execution**:
  - Refactor `analytica/agents/factory/chains.py` to use lazy functions (`get_supervisor_chain()`) rather than module-level variables.
- [ ] **1.2 Create Unified Agent Factory**:
  - Implement `create_agent_chain()` in `analytica/agents/common/builder.py` to eliminate duplicated LLM loader code.
- [ ] **1.3 Consolidate Schema Placement**:
  - Decide on a single consistent location for schemas (colocated in `agents/<agent_name>/schemas.py` or centralized in `analytica/schema/`).
  - Remove empty or redundant proxy `schema.py` files.

### Phase 2: Context-Aware Supervisor & State Alignment
- [ ] **2.1 Enhance Supervisor Prompt Inputs**:
  - Update `supervisor_prompt` template in `analytica/agents/supervisor/chain.py` to accept `dataset_metadata`, `execution_history`, and `previous_results`.
- [ ] **2.2 Refine `SupervisorOutput`**:
  - Add fields for `reasoning`, `is_replan`, and ensure `NextAction` enum strings match LangGraph node names 1-to-1.
- [ ] **2.3 Add Prompt Context Serializers**:
  - Implement helper functions to cleanly serialize dataset summaries and past agent findings into Markdown for prompt injection.

### Phase 3: Implementing Downstream Specialized Agents
- [ ] **3.1 Implement Data Analyst Agent**:
  - Add `prompts/data_analyst_prompt.md` and schema for profiling, missing values, and column selection.
- [ ] **3.2 Implement Statistical Analyst Agent**:
  - Add statistical procedure selection prompt and schema (hypothesis testing, correlations, parametric vs non-parametric).
- [ ] **3.3 Implement Visualization Agent**:
  - Add prompt and schema specifying chart type, x/y variables, and title.
- [ ] **3.4 Implement Critic Agent**:
  - Add validation prompt and schema with `is_valid: bool`, `confidence_score: float`, and `critique: str`.
- [ ] **3.5 Implement Interpretation Agent**:
  - Add prompt and schema for translating empirical stats into human-readable takeaways.
- [ ] **3.6 Implement Report Generation Agent**:
  - Add prompt and schema for assembling final executive report.

### Phase 4: Python Analysis Subgraph & Safe Execution
- [ ] **4.1 Code Generator & AST Validator**:
  - Create isolated sub-chain to generate Python scripts.
  - Add AST-based syntax and security checks (block dangerous operations like `os.system`).
- [ ] **4.2 Execution Sandbox & Self-Healing Loop**:
  - Execute code against the uploaded dataframe in a controlled environment.
  - On exception, route traceback to a Code Repair prompt with a max retry limit (e.g., 3 attempts).

### Phase 5: LangGraph Parent Graph & State Integration
- [ ] **5.1 Define `AnalyticaState` TypedDict**:
  - Define shared state (`user_query`, `dataset_path`, `dataset_metadata`, `supervisor_decision`, `agent_results`, `artifacts`, `final_report`).
- [ ] **5.2 Implement Generic Node Adapters**:
  - Wrap agent chains with `make_agent_node()` in `analytica/orchestration/nodes/`.
- [ ] **5.3 Assemble StateGraph**:
  - Connect Supervisor $\rightarrow$ Nodes $\rightarrow$ Critic $\rightarrow$ Report with conditional replanning edges.

### Phase 6: Streamlit UI Integration
- [ ] **6.1 Streamlit Event Callbacks**:
  - Hook into LangGraph state updates to stream agent progress and rendered charts to the UI.
