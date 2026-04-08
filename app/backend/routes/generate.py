from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from ai_engine.generator import generate_website

router = APIRouter()

@router.post("/api/generate")
def generate(data: dict):
    description = data.get("description", "No description")

    html_content = generate_website(description)

    with open("output.html", "w", encoding="utf-8") as f:
        f.write(html_content)

    return HTMLResponse(content=html_content)
