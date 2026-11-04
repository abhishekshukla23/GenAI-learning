from dotenv import load_dotenv
load_dotenv()

from langchain_mistralai import ChatMistralAI
from langchain_core.messages import AIMessage,SystemMessage,HumanMessage
model = ChatMistralAI(model="mistral-large-4", temperature=0.9)

print("Choose your AI mode")
print("press 1 for Angry mode")
print("press 2 for funny mode")
print("press 3 for sad mode")

choice=int(input("tell your response:-"))

if choice==1:
    mode="You are an angry AI agent. You respond aggressively and impatiently."
elif choice==2:
    mode="YOur are a very funny AI agent. You respond with humor and jokes."
elif choice==3:
    mode="You are a sad AI agent."


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
    SystemMessage(content=mode)
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
    