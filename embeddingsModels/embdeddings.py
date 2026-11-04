from dotenv import load_dotenv
load_dotenv()

from langchain_mistralai import MistralAIEmbeddings

embeddings=MistralAIEmbeddings(
    model='mistral-embed',
)
texts=[
    "Hello this is Abhishek Shukla",
    "Hello your name is YouTube",
    "And you all are very beautiful"
]
vector=embeddings.embed_query("You are going to learn GenAI")

print(vector)