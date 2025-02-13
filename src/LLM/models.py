from langchain_ollama import ChatOllama

def chat_model(model_name:str="mistral"):
    # Load the chat model from OllamaLLM
    print("🧠 Loading OllamaLLM Chat Model...\n")
    chat_model = ChatOllama(model=model_name)
    print(f"✅ Ollama {model_name} with 1.5B Parameters model loaded successfully.\n")
    return chat_model