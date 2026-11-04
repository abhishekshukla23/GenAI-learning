from dotenv import load_dotenv
load_dotenv()

from langchain_mistralai import ChatMistralAI
from langchain_core.messages import AIMessage,SystemMessage,HumanMessage
model = ChatMistralAI(model="mistral-large-4", temperature=0.9)


def extract_content(content):
  
    if isinstance(content, list):
        text_parts = [
            block.get("text", "") 
            for block in content 
            if isinstance(block, dict) and block.get("type") == "text"
        ]
        return "".join(text_parts).strip()
    
  
    return str(content)

messages=[
    SystemMessage(content="You are a funny AI agent")
]
while True:
    print("--------WELCOME___PRESS 0 TO EXIT--------")
    prompt = input("You: ")
    messages.append(HumanMessage(content=prompt))
    if prompt == "0":
        break

    response = model.invoke(messages)
    messages.append(AIMessage(content=extract_content(response.content)))


    print("Bot: ",extract_content(response.content))
    