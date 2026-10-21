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

    if question.lower() in ["exit", "quit"]:
        break

    # --------------------------
    # Intent Detection
    # --------------------------

    prompt = f"""
You are a classifier.

User question:
{question}

If the question is about:
- firewall
- firewalls
- firewall status
- firewall details
- online firewalls
- Sophos firewall

Reply ONLY:

FIREWALL

Otherwise reply ONLY:

GENERAL
"""

    intent_response = llm.invoke(
        [HumanMessage(content=prompt)]
    )

    intent = intent_response.content.strip().upper()

    print(f"\nIntent = {intent}\n")

    # --------------------------
    # Firewall Request
    # --------------------------

    if intent == "FIREWALL":

        try:

            result = requests.get(
                "http://127.0.0.1:8000/firewalls"
            )

            firewall_data = result.json()

            summary_prompt = f"""
You are a network engineer.

Summarize the following firewall data in a human readable format.

{firewall_data}
"""

            summary = llm.invoke(
                [HumanMessage(content=summary_prompt)]
            )

            print(summary.content)

        except Exception as e:

            print("FastAPI Error:", e)

    # --------------------------
    # General Question
    # --------------------------

    else:

        response = llm.invoke(
            [HumanMessage(content=question)]
        )

        print(response.content)

    print("\n" + "-" * 60 + "\n")