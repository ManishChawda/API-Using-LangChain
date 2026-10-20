from langchain.tools import tool
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import requests
import os

load_dotenv()


@tool
def get_os_info():
    """Get Windows OS information"""

    response = requests.get(
        "http://127.0.0.1:8000/os-info"
    )

    return response.json()


llm = ChatGroq(
    model="openai/gpt-oss-120b",
    api_key= os.getenv("GROQ_API_KEY")
)

tools = [get_os_info]

llm_with_tools = llm.bind_tools(tools)

question = input("Ask: ")

response = llm_with_tools.invoke(question)

print("\nLLM Response:")
print(response)

if response.tool_calls:

    print("\nTool Selected!")

    for tool_call in response.tool_calls:

        if tool_call["name"] == "get_os_info":

            result = get_os_info.invoke({})

            print("\nTool Result:")
            print(result)