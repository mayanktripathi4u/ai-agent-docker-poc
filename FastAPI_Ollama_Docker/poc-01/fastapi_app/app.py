from fastapi import FastAPI, Response
import requests

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI & Ollama in Docker: Demo! Use the /ask endpoint to ask a question to the llama3.2 model."}

@app.get("/ask")
def ask_ollama(question: str):
    print(f"Received question: {question}")

    OLLAMA_URL = "http://ollama:11434/api/generate"
    res = requests.post(OLLAMA_URL, json={
        "model": "llama3.2",
        "prompt": question,
        "stream": False
    })

    print(f"Ollama response status code: {res.status_code}")
    print(f"Ollama response content: {res.text}")

    return Response(
        content=res.text,
        media_type="application/json"
    )