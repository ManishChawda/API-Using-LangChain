from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
import requests
import os

load_dotenv()

# --------------------------
# LLM Setup
# --------------------------
llm = ChatGroq(
    model="openai/gpt-oss-120b",
    api_key=os.getenv("GROQ_API_KEY")
)

# --------------------------
# LLM Setup
# --------------------------
while True:

    question = input("Ask: ")

    if "firewall" in question.lower():

        result = requests.get(
            "http://127.0.0.1:8000/firewalls"
        )

        print(result.json())

    else:

        response = llm.invoke(
            [HumanMessage(content=question)]
        )

        print(response.content)