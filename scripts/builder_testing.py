import sys

from rich import print

from analytica.agents.schema import SupervisorOutput
from analytica.builder.agent_builder import AgentBuilder
from analytica.exception import AnalyticaException

try:
    obj = AgentBuilder(
        agent_prompt_name="supervisor_prompt",
        agent_name="supervisor_agent",
        agent_input_variables=["input"],
        agent_provider="groq",
        agent_schema=SupervisorOutput,
    )
except Exception as e:
    raise AnalyticaException(error=e, error_detail=sys)
else:
    chain = obj.build_agent_chain()
    txt = """I am evaluating whether a company should expand its AI-powered fraud detection platform into the European market.

Analyze the following situation:

The company currently operates in India and has a fraud detection system that processes transaction data, customer behavioral data, and identity verification information. The system uses an ensemble of machine learning models and an LLM-based investigation assistant.

For the European expansion, I need to determine:

1. Which GDPR requirements could affect the collection, processing, storage, and transfer of customer and transaction data.
2. Whether using an LLM for fraud-investigation summaries introduces additional privacy or compliance risks.
3. What data should be stored, what should be anonymized or pseudonymized, and what should not be retained.
4. Whether the existing ML fraud model is likely to suffer from distribution shift when deployed on European transaction data.
5. Which statistical and ML analyses should be performed before deployment to determine whether the model needs retraining.
6. How model performance should be evaluated across different customer segments without creating unfair or discriminatory outcomes.
7. What technical architecture would allow the system to process sensitive data while minimizing unnecessary exposure to third-party LLM providers.
8. Finally, produce a phased implementation plan covering compliance assessment, data analysis, model validation, architecture changes, and production deployment.

Do not perform the analysis yourself. Determine which specialized agents should handle each part of the problem and specify the order in which they should be executed. Identify dependencies between tasks and explain which tasks can be performed in parallel."""

    input = {obj.agent_input_variables[0]: txt}
    res = chain.invoke(input=input)
    print(res)
