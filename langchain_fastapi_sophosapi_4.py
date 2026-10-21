from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
import requests
import os
import json

load_dotenv()

# ==========================================
# LLM Setup
# ==========================================

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    api_key=os.getenv("GROQ_API_KEY")
)

print("\nType exit or quit to stop.\n")

# ==========================================
# Main Loop
# ==========================================

while True:

    question = input("Ask: ")

    # --------------------------------------
    # Exit
    # --------------------------------------

    if question.lower() in ["exit", "quit"]:
        print("Goodbye")
        break

    # --------------------------------------
    # Intent + Parameter Extraction
    # --------------------------------------

    classifier_prompt = f"""
You are an intent extractor.

Analyze the user question and return ONLY valid JSON.

Format:

{{
    "intent": "FIREWALL" or "GENERAL",
    "location": ""
}}

Rules:

1. Firewall-related questions:
   - show firewalls
   - list firewalls
   - firewall status
   - firewall details
   - online firewalls
   - show firewall in GRKL
   - show firewall in Mumbai
   - show MCP firewall

Return:
{{
    "intent":"FIREWALL",
    "location":"<location if present>"
}}

2. Any other question:

Return:
{{
    "intent":"GENERAL",
    "location":""
}}

User Question:

{question}
"""

    try:

        intent_response = llm.invoke(
            [HumanMessage(content=classifier_prompt)]
        )

        raw_output = intent_response.content.strip()

        print("\nRaw LLM Output:")
        print(raw_output)

        parsed = json.loads(raw_output)

        intent = parsed.get("intent", "GENERAL")
        location = parsed.get("location", "")

    except Exception as e:

        print("\nJSON Parse Error:", str(e))

        intent = "GENERAL"
        location = ""

    print("\nIntent =", intent)
    print("Location =", location)

    # --------------------------------------
    # Firewall Requests
    # --------------------------------------

    if intent == "FIREWALL":

        if location:

            url = (
                f"http://127.0.0.1:8000/firewalls"
                f"?location={location}"
            )

        else:

            url = "http://127.0.0.1:8000/firewalls"

        print("\nCalling FastAPI:")
        print(url)

        try:

            result = requests.get(url)

            print("\nHTTP Status =", result.status_code)

            if result.status_code != 200:

                print("\nFastAPI Error:")
                print(result.text)

                print("\n" + "-" * 60 + "\n")
                continue

            firewall_data = result.json()

            summary_prompt = f"""
You are a Sophos firewall assistant.

Summarize this firewall data.

Mention:

- Firewall Name
- Model
- WAN IP Addresses
- Online Status

Firewall Data:

{firewall_data}
"""

            summary = llm.invoke(
                [HumanMessage(content=summary_prompt)]
            )

            print("\n" + summary.content)

        except Exception as e:

            print("\nFastAPI Error:", str(e))

    # --------------------------------------
    # General Questions
    # --------------------------------------

    else:

        try:

            response = llm.invoke(
                [HumanMessage(content=question)]
            )

            print("\n" + response.content)

        except Exception as e:

            print("\nLLM Error:", str(e))

    print("\n" + "-" * 60 + "\n")