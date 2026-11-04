from dotenv import load_dotenv
from pathlib import Path
from langchain.chat_models import init_chat_model
load_dotenv()
# model = ChatGoogleGenerativeAI(
#     model="gemini-3.8-flash"
# )

# model=init_chat_model("groq:openai/gpt-oss-120b")

# response = model.invoke("Why do parrots talk?")
# print(response.content)


# from langchain_groq import ChatGroq

# model=ChatGroq(model="openai/gpt-oss-120b")
# response = model.invoke("Why do parrots talk?")
# print(response.content)

from langchain_mistralai import ChatMistralAI

model=ChatMistralAI(model="mistral-large-4",temperature=0.9)

response = model.invoke("write a poem")
print(response.content)