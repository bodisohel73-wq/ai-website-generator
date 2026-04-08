from fastapi import APIRouter

router = APIRouter(
    prefix="/api/projects",
    tags=["projects"]
)

@router.get("/")
async def get_projects():
    return {
        "message": "Projects route working",
        "status": "success"
    }
