# 📊 Analytica: Local Multi-Agent AI Data Analysis System

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![LangGraph](https://img.shields.io/badge/Orchestration-LangGraph-FF6F00?style=for-the-badge&logo=langchain&logoColor=white)](https://langchain-ai.github.io/langgraph/)
[![LangChain](https://img.shields.io/badge/Framework-LangChain-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)](https://langchain.com)
[![Groq](https://img.shields.io/badge/Inference-Groq-F05A28?style=for-the-badge&logo=fastapi&logoColor=white)](https://groq.com)
[![Streamlit](https://img.shields.io/badge/UI-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Docker](https://img.shields.io/badge/Deployment-Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com)
[![Ruff](https://img.shields.io/badge/Linter-Ruff-FCC21B?style=for-the-badge&logo=ruff&logoColor=black)](https://astral.sh/ruff)
[![uv](https://img.shields.io/badge/Packaging-uv-DE5FE9?style=for-the-badge&logo=astral&logoColor=white)](https://astral.sh/uv)

<p align="center">
  <strong>Autonomous, evidence-backed data analysis combining multi-agent LLM reasoning with deterministic Python execution.</strong>
</p>

</div>

---

## 📑 Table of Contents

- [🎯 1. Overview](#-1-overview)
- [🧩 2. Problem Statement & Solution](#-2-problem-statement--solution)
- [💡 3. Core Philosophy](#-3-core-philosophy)
- [🏛️ 4. High-Level Architecture](#️-4-high-level-architecture)
- [🤖 5. Agent Architecture](#-5-agent-architecture)
- [⚡ 6. Python Analysis Subgraph](#-6-python-analysis-subgraph)
- [🔄 7. LangGraph Orchestration Layer](#-7-langgraph-orchestration-layer)
- [⚙️ 8. Core & Provider Infrastructure](#️-8-core--provider-infrastructure)
- [🛠️ 9. Technology Stack](#️-9-technology-stack)
- [📂 10. Project Organization](#-10-project-organization)
- [🚀 11. Quickstart & Local Setup](#-11-quickstart--local-setup)
- [🐳 12. Docker Deployment](#-12-docker-deployment)
- [🌟 13. What Makes Analytica Different](#-13-what-makes-analytica-different)
- [🎯 14. Current Scope & Boundaries](#-14-current-scope--boundaries)

---

## 🎯 1. Overview

**Analytica** is a local, containerized, multi-agent AI data-analysis platform. It bridges the gap between high-level analytical questions and rigorous data exploration.

### 📥 What the User Provides
1. **Dataset**: Structured tabular data (CSV, Parquet, Excel).
2. **Analytical Objective**: Natural-language analytical question or research hypothesis.

### 📤 What Analytica Delivers
* Autonomous decomposition of the analytical objective into a structured execution plan.
* Delegation across specialized agents for data profiling, statistical modeling, and visualization.
* Deterministic Python execution in a validated sandbox.
* Quality control and critique loop to verify evidence and prevent hallucination.
* An interactive, evidence-backed final analytical report delivered via a **Streamlit UI**.

```text
                 USER
                  │
                  │ (Dataset + Natural Language Query)
                  ▼
          ┌─────────────────┐
          │  Streamlit UI   │
          └────────┬────────┘
                   │
                   ▼
          ┌─────────────────┐
          │    Analytica    │
          │  Parent Graph   │
          └────────┬────────┘
                   │
                   ▼
       Comprehensive Final Report
```

> [!NOTE]
> **Zero API Overhead**: Analytica is delivered as a fully containerized Docker image running both the backend LangGraph orchestration and the Streamlit frontend.

---

## 🧩 2. Problem Statement & Solution

Traditional data analysis is a time-consuming, fragmented, and error-prone process:

```text
Load Data → Understand Schema → Clean Data → Explore Data → Run Statistics → Plot Charts → Interpret Findings → Write Report
```

### ❌ Challenges in Traditional Workflows
* **High Manual Overhead**: Repetitive exploratory and data-cleaning code.
* **Skill Bottlenecks**: Requires deep expertise across data engineering, statistical inference, and visualization.
* **LLM Hallucinations**: Standard LLM-based "Chat with CSV" tools frequently invent numbers, misunderstand distributions, or generate unverified code.
* **Unvalidated Assumptions**: Inappropriate statistical tests (e.g., applying parametric tests to skewed distributions).

### ✅ The Analytica Solution
* **Specialized Agent Delegation**: Individual agents specialize in dedicated steps (Profiling, Statistics, Visuals, Quality Control).
* **Deterministic Code Execution**: Computations, correlations, and plots are executed exclusively by Python libraries (Pandas, SciPy, Matplotlib), never hallucinated by the LLM.
* **Closed-Loop Verification**: A dedicated **Critic Agent** inspects analytical artifacts against claims before final report generation.

---

## 💡 3. Core Philosophy

Analytica operates on strict separation of concerns:

$$ \text{LLM} \rightarrow \text{Reasoning} \quad\Big|\quad \text{Python} \rightarrow \text{Computation} $$

```text
┌──────────────────────────────────────────────────────────┐
│  LLM (Reasoning & Strategy)                              │
│  • Interprets user intent                                │
│  • Decides statistical procedures and chart types        │
│  • Evaluates findings and explains contextual impact     │
└────────────────────────────┬─────────────────────────────┘
                             │ Delegates computation
                             ▼
┌──────────────────────────────────────────────────────────┐
│  Python (Deterministic Computation)                      │
│  • Computes exact mathematical values (e.g., p-values)   │
│  • Executes matrix operations and aggregations           │
│  • Renders reproducible visualization files              │
└──────────────────────────────────────────────────────────┘
```

---

## 🏛️ 4. High-Level Architecture

```text
                         ┌──────────────┐
                         │     USER     │
                         └──────┬───────┘
                                │ Dataset + Question
                                ▼
                     ┌──────────────────┐
                     │   STREAMLIT UI   │
                     └────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │   PARENT GRAPH    │
                    │   (Supervisor)    │
                    └─────────┬─────────┘
                              │ Analysis Plan
            ┌─────────────────┼──────────────────┐
            ▼                 ▼                  ▼
      DATA ANALYST      STATISTICAL        VISUALIZATION
         AGENT            ANALYST              AGENT
            │                 │                  │
            └─────────────────┼──────────────────┘
                              │ Code Instructions
                              ▼
                  ┌─────────────────────┐
                  │   PYTHON ANALYSIS   │
                  │      SUBGRAPH       │
                  └──────────┬──────────┘
                             │ Generated Artifacts (Data, Plots, Stats)
                             ▼
                  ┌─────────────────────┐
                  │    CRITIC AGENT     │
                  │    (Validation)     │
                  └──────────┬──────────┘
                             │
                       ┌─────┴─────┐
                       │           │
                   [Invalid]    [Valid]
                       │           │
                       ▼           ▼
                  Re-analyze  INTERPRETATION
                                  AGENT
                                    │
                                    ▼
                            REPORT GENERATION
                                  AGENT
                                    │
                                    ▼
                              FINAL REPORT
```

---

## 🤖 5. Agent Architecture

Analytica uses a focused team of specialized agents, each constrained to its core domain:

| Agent | Core Responsibility | Key Outputs |
| :--- | :--- | :--- |
| **🧠 Supervisor** | Workflow planning, goal decomposition, agent routing | Structured Analysis Plan |
| **🔍 Data Analyst** | Schema understanding, missing values, cardinality, outliers | Dataset Profile & Quality Report |
| **📈 Statistical Analyst** | Hypothesis testing, correlation analysis, significance tests | Statistical Plan & Test Specs |
| **🎨 Visualization** | Chart selection (scatter, box, KDE), aesthetic parameters | Visualization Specs & Scripts |
| **💡 Interpretation** | Explains empirical evidence, limitations, and key drivers | Human-Readable Analytical Findings |
| **🛡️ Critic** | Quality control, numerical consistency, claim verification | Validation Verdict (Pass / Retry) |
| **📝 Report Generator** | Synthesis of findings, charts, and methodology | Polished Final Analytical Report |

---

## ⚡ 6. Python Analysis Subgraph

The **Python Analysis Subgraph** is an isolated execution engine that turns natural-language analytical tasks into verified Python computations:

```text
                 Analytical Instruction
                           │
                           ▼
                  ┌────────────────┐
                  │ Code Generator │ (Generates Python script)
                  └───────┬────────┘
                          │
                          ▼
                  ┌────────────────┐
                  │ Code Validator │ (AST security & import safety checks)
                  └───────┬────────┘
                          │
                          ▼
                  ┌────────────────┐
                  │ Python Executor│ (Executes in dedicated workspace)
                  └───────┬────────┘
                          │
                          ▼
                  ┌────────────────┐
                  │Output Validator│ (Checks outputs & return codes)
                  └───────┬────────┘
                          │
                       ┌──┴──┐
                     [Error] [Valid]
                       │       │
                       ▼       ▼
                    Repair   Return Artifacts
                       │
                       └───→ Re-execute
```

* **Self-Healing Loop**: If Python encounters a runtime error (e.g., `KeyError` or dimension mismatch), the error traceback is routed back to the Code Generator for automated repair.
* **Deterministic Artifact Storage**: Execution results, summaries, and images are written to persistent storage paths.

---

## 🔄 7. LangGraph Orchestration Layer

The workflow is orchestrated using **LangGraph**, keeping agent logic decoupled from workflow topology.

```text
src/analytica/
├── agents/            # Isolated agent logic (prompts, schemas, execution)
│   ├── supervisor/
│   ├── data_analyst/
│   ├── statistical_analyst/
│   ├── visualisation/
│   ├── interpretation/
│   ├── critic/
│   └── report_generation/
│
└── orchestration/     # LangGraph integration
    ├── state/         # Shared TypedDict / Pydantic state
    ├── nodes/         # State adapters wrapping agents
    ├── edges/         # Conditional routing logic
    ├── subgraphs/     # Nested graphs (e.g., Python execution)
    └── graphs/        # Parent compiled workflow
```

### 📦 Workflow State (`AnalyticaState`)
* `user_query`: Original natural language question.
* `dataset_metadata`: Schema, shape, and column summaries.
* `analysis_plan`: Ordered list of tasks determined by the Supervisor.
* `agent_results`: Structured task outputs from specialized agents.
* `artifacts`: Filepaths of generated plots, tables, and computed metrics.
* `validation_results`: Critic feedback, scores, and status flags.
* `final_report`: Markdown-formatted final analytical deliverable.

---

## ⚙️ 8. Core & Provider Infrastructure

Analytica features a decoupled LLM provider architecture built on **Groq** for high-throughput inference:

```text
config/llm_provider.yaml  ──►  Pydantic Settings  ──►  ProviderFactory  ──►  ChatGroq Instance
                                      ▲
.env (GROQ_API_KEY) ──────────────────┘
```

* **Secret Separation**: API keys (`GROQ_API_KEY`) are managed exclusively via `.env` and Pydantic `SecretStr`.
* **Provider Configuration**: Model names, temperature, tokens, and retries are managed per-agent in `config/llm_provider.yaml`.
* **Model Routing**: High-reasoning agents (Supervisor, Critic) utilize larger models, while focused tasks utilize lightweight models.

---

## 🛠️ 9. Technology Stack

| Category | Technology | Purpose |
| :--- | :--- | :--- |
| **Language** | **Python 3.12+** | Core runtime |
| **Orchestration** | **LangGraph** | Multi-agent state machines, conditional routing, subgraphs |
| **LLM Framework** | **LangChain** | Chat model abstraction, structured outputs, prompt management |
| **Inference Provider**| **Groq** | Ultra-low latency LLM inference |
| **Computation** | **Pandas, NumPy, SciPy, Scikit-Learn** | Deterministic mathematical and statistical calculations |
| **Visualization** | **Matplotlib, Seaborn, Plotly** | Automated chart rendering and graphic artifacts |
| **Configuration** | **Pydantic, Pydantic-Settings, PyYAML** | Type-safe schema validation and environment management |
| **User Interface** | **Streamlit** | Interactive web UI for dataset upload and report presentation |
| **Tooling & Packaging**| **uv, Ruff** | Package management, fast virtual environments, code linting |
| **Containerization** | **Docker** | Reproducible standalone deployment |

---

## 📂 10. Project Organization

```text
analytica/
├── config/
│   └── llm_provider.yaml      <- Provider & agent model parameters
│
├── data/
│   ├── raw/                   <- Uploaded source datasets
│   ├── interim/               <- Intermediate cleaned frames
│   └── processed/             <- Final data artifacts
│
├── log/                       <- Plaintext application execution logs
├── models/                    <- Serialized models and artifacts
├── reports/
│   └── figures/               <- Generated plots and graphics
│
├── analytica/
│   ├── core/                  <- Global configs, constants, and paths
│   │   ├── config/            <- Root directory and runtime variable configs
│   │   └── constants/         <- Path, project, and provider constants
│   ├── providers/             <- LLM provider abstractions and Groq factory
│   ├── logger/                <- Colored console & rotating file logging
│   ├── exception/             <- Custom exception handler with auto-traceback
│   └── utils/                 <- Project root resolution & YAML loaders
│
├── tests/                     <- Comprehensive unit and integration test suite
├── pyproject.toml             <- Dependencies, project metadata, and Ruff config
├── uv.lock                    <- Deterministic dependency lockfile
└── README.md                  <- Project documentation
```

---

## 🚀 11. Quickstart & Local Setup

### 📋 Prerequisites
* **Python 3.12+**
* [**uv**](https://docs.astral.sh/uv/) (recommended package manager)
* **Groq API Key** ([Get one here](https://console.groq.com/))

### 🔧 1. Clone & Install Dependencies
```bash
git clone https://github.com/gauravgulia26/analytica.git
cd analytica

# Create virtual environment and install all dependencies
uv sync
```

### 🔑 2. Environment Configuration
Create a `.env` file in the project root:
```bash
cp .env.example .env
```
Add your credentials:
```ini
GROQ_API_KEY=gsk_your_actual_groq_api_key_here
ANALYTICA_ENV=development
LOG_LEVEL=INFO
DEBUG=False
```

### 🧪 3. Run Quality Checks & Tests
```bash
# Run unit and integration tests
uv run pytest

# Check formatting and linting
uv run ruff check .
```

### 🖥️ 4. Launch the Streamlit Interface
```bash
uv run streamlit run src/analytica/ui/streamlit_app.py
```

---

## 🐳 12. Docker Deployment

Analytica is built for zero-dependency containerized execution.

### 🏗️ Build the Docker Image
```bash
docker build -t analytica:latest .
```

### 🚀 Run the Container
```bash
docker run -d \
  -p 8501:8501 \
  --env-file .env \
  --name analytica-app \
  analytica:latest
```

Open your browser at `http://localhost:8501` to access the Streamlit UI.

---

## 🌟 13. What Makes Analytica Different

* 🧩 **True Multi-Agent Specialization**: Distinct agents handle planning, stats, visuals, and synthesis rather than a single massive prompt.
* 🔢 **Deterministic Number Generation**: The LLM never invents numbers; Python calculates all metrics and significance levels.
* 🔁 **Autonomous Self-Correction**: Code execution failures automatically trigger traceback-guided code repairs.
* 🛡️ **Evidence-Backed Validation**: The Critic Agent prevents hallucinations by cross-checking conclusions against computed artifacts.
* 🔌 **Provider-Agnostic Core**: Modular provider factory decouples LLM inference from agent logic.

---

## 🎯 14. Current Scope & Boundaries

### ✅ In-Scope
* Multi-Agent LangGraph Workflow (Supervisor, Profiler, Statistician, Visualizer, Critic, Reporter).
* Automated Python code generation, sandboxed execution, and repair loop.
* Groq LLM inference integration with YAML/Pydantic configuration.
* Streamlit interactive UI with report export.
* Standalone Docker image deployment.

### ⛔ Explicitly Out of Scope (Phase 1)
* Machine Learning model training / AutoML agents.
* REST API / FastAPI backend endpoints.
* Distributed cloud Kubernetes deployments.
* Multi-user database authentication.

---

<div align="center">
  <sub>Built with ❤️ by the Analytica Team. Distributed under the MIT License.</sub>
</div>
