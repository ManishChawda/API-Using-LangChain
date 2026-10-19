from langchain.tools import tool
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import requests
import os


@tool
def get_os_info():
    """Get Windows operating system information"""

    response = requests.get(
        "http://127.0.0.1:8000/os-info"
    )

    return response.json()


@tool
def get_memory_info():
    """Get Windows memory information"""

    response = requests.get(
        "http://127.0.0.1:8000/memory"
    )

    return response.json()


llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    GROQ_API_KEY= os.getenv("GROQ_API_KEY")
)

tools = [
    get_os_info,
    get_memory_info
]

tool_map = {
    "get_os_info": get_os_info,
    "get_memory_info": get_memory_info
}

llm_with_tools = llm.bind_tools(tools)

while True:

    question = input("\nAsk: ")

    if question.lower() == "exit":
        break

    response = llm_with_tools.invoke(question)

    print("\nTool Calls:")
    print(response.tool_calls)

    if response.tool_calls:

        for tool_call in response.tool_calls:

            tool_name = tool_call["name"]

            result = tool_map[tool_name].invoke({})

            print("\nResult:")
            print(result)

    else:

        print("\nLLM Answer:")
        print(response.content)
