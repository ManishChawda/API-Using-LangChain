from langchain.tools import tool
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import requests
import os

load_dotenv()

@tool
def get_os_info():
    """
    Returns operating system information from FastAPI.
    """

    response = requests.get(
        "http://127.0.0.1:8000/os-info"
    )

    return str(response.json())


llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    GROQ_API_KEY= os.getenv("GROQ_API_KEY")
    )

question = input("Ask Question: ")

if "os" in question.lower():
    result = get_os_info.invoke({})
    print(result)
else:
    print(llm.invoke(question).content)
