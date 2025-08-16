import os, json
from typing import List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx

app = FastAPI(title="Sala de IAs – Hub")
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "*").split(","),
    allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
ENABLE_OPENAI = os.getenv("ENABLE_OPENAI", "false").lower() == "true"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class ChatIn(BaseModel):
    model_config = {"protected_namespaces": ()}
    message: str
    model_ollama: str = "llama3.1:8b"
    use_openai: bool = False
    openai_model: str = "gpt-4o-mini"

class AgentReply(BaseModel):
    agent: str
    text: str

class ChatOut(BaseModel):
    replies: List[AgentReply]

async def call_ollama(prompt: str, model: str) -> str:
    async with httpx.AsyncClient(timeout=120) as client:
        r = await client.post(f"{OLLAMA_URL}/api/generate", json={"model": model, "prompt": prompt})
        if r.status_code != 200:
            raise HTTPException(502, f"Ollama erro: {r.text}")
        text = ""
        for line in r.text.splitlines():
            try:
                obj = json.loads(line)
                text += obj.get("response", "")
            except Exception:
                pass
        return text.strip()

async def call_openai(prompt: str, model: str) -> str:
    if not (ENABLE_OPENAI and OPENAI_API_KEY):
        raise HTTPException(400, "OpenAI desativado ou sem chave")
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type": "application/json"}
    payload = {"model": model, "messages": [{"role": "user", "content": prompt}], "temperature": 0.7}
    async with httpx.AsyncClient(timeout=120) as client:
        r = await client.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        if r.status_code != 200:
            raise HTTPException(502, f"OpenAI erro: {r.text}")
        data = r.json()
        return data["choices"][0]["message"]["content"].strip()

@app.post("/chat", response_model=ChatOut)
async def chat(body: ChatIn):
    replies: List[AgentReply] = []
    ollama_text = await call_ollama(body.message, body.model_ollama)
    replies.append(AgentReply(agent=f"ollama:{body.model_ollama}", text=ollama_text))
    if body.use_openai:
        try:
            openai_text = await call_openai(body.message, body.openai_model)
            replies.append(AgentReply(agent=f"openai:{body.openai_model}", text=openai_text))
        except HTTPException as e:
            replies.append(AgentReply(agent=f"openai:{body.openai_model}", text=f"[erro] {e.detail}"))
    return ChatOut(replies=replies)

@app.get("/")
async def root():
    return {"ok": True, "service": "Sala de IAs – Hub"}
