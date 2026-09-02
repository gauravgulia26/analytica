import sys

from rich import print

from analytica.agents.factory.chains import load_supervisor_chain
from analytica.exception.custom_exception import AnalyticaException


def main():
    try:
        chain = load_supervisor_chain()
    except Exception as e:
        raise AnalyticaException(error=e, error_detail=sys)
    else:
        test_input = {"user_query": """
    I have uploaded a customer dataset. I want to understand why customers are
    churning. First inspect the dataset and identify the relevant variables.
    Then analyze the relationship between those variables and churn, perform
    appropriate statistical analysis, create useful visualizations, validate
    the findings, and summarize the key insights.
    """}
        res = chain.invoke({"user_query": test_input})
        print(res)


if __name__ == "__main__":
    main()
