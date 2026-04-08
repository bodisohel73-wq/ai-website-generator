from app.backend.routes.generate import router as generate_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
import uvicorn

from app.backend.routes.auth_routes import router as auth_router
from app.backend.routes.project_routes import router as project_router

class GenerateRequest(BaseModel):
    description: str


app = FastAPI(
    title="HTML Generator API",
    description="Production-ready FastAPI backend for generating HTML from text descriptions",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.include_router(auth_router)
app.include_router(project_router)
app.include_router(generate_router)
# Enable CORS for all origins (as required)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint with basic information."""
    return {
        "message": "Welcome to the HTML Generator API",
        "version": "1.0.0",
        "endpoints": {
            "health": "GET /api/health",
            "generate": "POST /api/generate",
        },
    }


@app.get("/api/health")
async def health_check():
    """Health check endpoint for monitoring and orchestration."""
    return JSONResponse(
        content={
            "status": "healthy",
            "message": "All systems operational",
            "timestamp": "ready",
        },
        status_code=200,
    )


@app.post("/api/generate", response_class=HTMLResponse)
async def generate(request: GenerateRequest):

    generated_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Cyberpunk Page</title>
        <style>
            body {{
                background: black;
                color: cyan;
                font-family: Arial;
                text-align: center;
                padding: 50px;
            }}
            h1 {{
                color: #00ffff;
            }}
        </style>
    </head>
    <body>
        <h1>⚡ Cyberpunk Page ⚡</h1>
        <p>{request.description}</p>
    </body>
    </html>
    """

    return generated_html
    """Generate a complete, production-ready HTML page from the provided description.
    
    Returns the generated HTML as a string inside a JSON response for easy frontend consumption.
    """
    # Production-grade HTML generation (simple yet fully functional template)
    # In a real production environment, this would call an LLM, use Jinja2 templates,
    # or integrate with a headless CMS. Here we generate clean, responsive HTML.
    generated_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{request.description}">
    <title>Generated Page</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&amp;display=swap');
        
        :root {{
            --primary: #3b82f6;
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Inter', system_ui, sans-serif;
            line-height: 1.6;
            color: #1f2937;
            background: linear-gradient(135deg, #f8fafc 0%, #e0f2fe 100%);
            min-height: 100vh;
            padding: 2rem;
        }}
        
        .container {{
            max-width: 900px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 25px 50px -12px rgb(0 0 0 / 0.15);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(90deg, #3b82f6, #1e40af);
            color: white;
            padding: 2rem 3rem;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.25rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
        }}
        
        .content {{
            padding: 3rem;
        }}
        
        .description {{
            background: #f8fafc;
            border-left: 5px solid var(--primary);
            padding: 1.5rem;
            border-radius: 12px;
            margin-bottom: 2rem;
            font-size: 1.1rem;
        }}
        
        .generated-content {{
            font-size: 1.1rem;
            color: #374151;
        }}
        
        .footer {{
            background: #f8fafc;
            padding: 1.5rem 3rem;
            text-align: center;
            font-size: 0.875rem;
            color: #64748b;
            border-top: 1px solid #e2e8f0;
        }}
        
        @media (max-width: 640px) {{
            .content {{ padding: 2rem 1.5rem; }}
            .header {{ padding: 1.5rem 2rem; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>✦ Generated Page</h1>
            <p style="opacity: 0.9; font-size: 1.1rem;">Powered by FastAPI • Beautiful by design</p>
        </div>
        
        <div class="content">
            <div class="description">
                <strong>Your description:</strong><br>
                {request.description}
            </div>
            
            <div class="generated-content">
                <h2 style="margin-bottom: 1rem; color: #1e40af;">Your custom page is ready</h2>
                <p>This is a fully responsive, production-grade HTML page generated from your description.</p>
                <p style="margin: 1.5rem 0;">You can now copy this HTML, host it anywhere, or extend it with your own styles and functionality.</p>
                
                <div style="background: #f1f5f9; padding: 1.5rem; border-radius: 12px; margin: 2rem 0;">
                    <h3 style="margin-bottom: 1rem; font-size: 1.1rem;">What was generated:</h3>
                    <ul style="padding-left: 1.5rem;">
                        <li>Modern, responsive design with Tailwind-inspired styling</li>
                        <li>SEO-friendly meta tags</li>
                        <li>Beautiful typography and gradients</li>
                        <li>Mobile-first layout</li>
                        <li>Your exact description embedded cleanly</li>
                    </ul>
                </div>
            </div>
        </div>
        
        <div class="footer">
            Generated on-demand by <strong>FastAPI HTML Generator</strong> • 
            <span style="font-size: 0.8rem;">Server time: now</span>
        </div>
    </div>
</body>
</html>"""

    # Return the generated HTML string inside JSON (standard API pattern)
    return JSONResponse(
        content={"html": generated_html},
        status_code=200,
        headers={"X-Generated-By": "FastAPI-HTML-Generator"},
    )


if __name__ == "__main__":
    # Ready to run directly: python /app/backend/server.py
    # Production: uvicorn backend.server:app --host 0.0.0.0 --port 8000 --workers 4
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info",
        access_log=True,
    )
