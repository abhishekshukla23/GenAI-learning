from dotenv import load_dotenv

load_dotenv()

from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint

llm = HuggingFaceEndpoint(
    repo_id="mistralai/Mistral-7B-Instruct-v0.3"
)

model = ChatHuggingFace(llm = llm)

response = model.invoke("Who are you?")

print(response.content)