from langchain_ollama import OllamaLLM

def get_reasoning_model():
    return OllamaLLM(model="qwen2.5:7b")

def get_coding_model():
    return OllamaLLM(model="deepseek-coder:6.7b")