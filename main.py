from rich import print
from rich.traceback import install

from analytica.providers.factory import ProviderFactory

install()


def main():
    obj = ProviderFactory(provider_name="groq", agent_name="supervisor_agent")
    llm = obj.get_llm()
    print(llm.invoke("hi"))


if __name__ == "__main__":
    main()
