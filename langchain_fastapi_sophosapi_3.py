from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
import requests
import os

load_dotenv()

# =====================================
# LLM Setup
# =====================================

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    GROQ_API_KEY= os.getenv("GROQ_API_KEY")
)

print("Type exit or quit to stop.\n")

# =====================================
# Main Loop
# =====================================

while True:

    question = input("Ask: ")

    # Exit
    if question.lower() in ["exit", "quit"]:
        print("Goodbye")
        break

    # =====================================
    # Intent + Location Detection
    # =====================================

    classifier_prompt = f"""
You are a classifier.

User question:
{question}

Return ONLY ONE of the following:

FIREWALL_ALL
FIREWALL_GRKL
FIREWALL_MCP
GENERAL

Examples:

show all firewalls
-> FIREWALL_ALL

which firewalls are online
-> FIREWALL_ALL

show GRKL firewall
-> FIREWALL_GRKL

show firewall in GRKL
-> FIREWALL_GRKL

show MCP firewall
-> FIREWALL_MCP

show firewall in MCP
-> FIREWALL_MCP

what is 2+2
-> GENERAL
"""

    intent_response = llm.invoke(
        [HumanMessage(content=classifier_prompt)]
    )

    intent = intent_response.content.strip().upper()

    print("\nIntent =", intent)

    # =====================================
    # FIREWALL ALL
    # =====================================

    if intent == "FIREWALL_ALL":

        url = "http://127.0.0.1:8000/firewalls"

    elif intent == "FIREWALL_GRKL":

        url = "http://127.0.0.1:8000/firewalls?location=GRKL"

    elif intent == "FIREWALL_MCP":

        url = "http://127.0.0.1:8000/firewalls?location=MCP"

    else:

        response = llm.invoke(
            [HumanMessage(content=question)]
        )

        print("\n" + response.content)
        print("\n" + "-" * 60 + "\n")
        continue

    # =====================================
    # FastAPI Call
    # =====================================

    try:

        result = requests.get(url)

        print("HTTP Status =", result.status_code)

        if result.status_code != 200:

            print("FastAPI returned error:")
            print(result.text)
            print("\n" + "-" * 60 + "\n")
            continue

        firewall_data = result.json()

        # =====================================
        # Summarize Using LLM
        # =====================================

        summary_prompt = f"""
You are a Sophos firewall assistant.

Summarize this firewall data.

Mention:
- Firewall name
- Model
- WAN IP addresses
- Online status

Firewall Data:

{firewall_data}
"""

        summary = llm.invoke(
            [HumanMessage(content=summary_prompt)]
        )

        print("\n" + summary.content)

    except Exception as e:

        print("\nFastAPI Error:", str(e))

    print("\n" + "-" * 60 + "\n")