from langchain_core.prompts import ChatPromptTemplate

from analytica.utils.loaders import load_prompt


def make_prompt_template(
    prompt_name: str,
    input_variables: list[str],
) -> ChatPromptTemplate:
    """Create a ChatPromptTemplate from a stored Markdown prompt."""

    prompt_text = load_prompt(prompt_name)

    human_template = "\n".join(f"{variable}: {{{variable}}}" for variable in input_variables)

    return ChatPromptTemplate.from_messages(
        [
            ("system", prompt_text),
            ("human", human_template),
        ]
    )
