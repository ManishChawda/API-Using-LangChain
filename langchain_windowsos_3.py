from langchain.tools import tool
from langchain_groq import ChatGroq
import requests


@tool
def get_os_info():
    """Get Windows OS information"""

    response = requests.get(
        "http://127.0.0.1:8000/os-info"
    )

    return str(response.json())


llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key="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"
)

tools = [get_os_info]

llm_with_tools = llm.bind_tools(tools)

question = input("Ask: ")

response = llm_with_tools.invoke(question)

print(response)