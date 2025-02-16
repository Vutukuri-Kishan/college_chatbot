import os
import uvicorn
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from chatbot import get_answer

app = FastAPI()

# Mount the 'static' folder for frontend files
static_dir = os.path.join(os.getcwd(), "static")
if not os.path.exists(static_dir):
    os.makedirs(static_dir)

app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    index_path = os.path.join(static_dir, "index.html")
    if not os.path.exists(index_path):
        return HTMLResponse(content="<h1>Static index.html not found</h1>", status_code=404)
    
    with open(index_path, "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    question = data.get("question", "")
    answer = get_answer(question)
    return {"answer": answer}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # Use environment variable for port
    uvicorn.run("app:app", host="0.0.0.0", port=port)
