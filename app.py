import os
import uvicorn
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from chatbot import get_answer

app = FastAPI()

# Ensure 'static' directory exists to prevent errors
if not os.path.exists("static"):
    os.makedirs("static")

# Mount the 'static' folder for frontend files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    index_path = "static/index.html"
    if not os.path.exists(index_path):
        return HTMLResponse(content="<h1>Frontend not found. Please deploy your static files.</h1>", status_code=404)
    
    with open(index_path, "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    question = data.get("question", "")
    answer = get_answer(question)
    return {"answer": answer}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # Use Render's assigned port
    uvicorn.run(app, host="0.0.0.0", port=port)
