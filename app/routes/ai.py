from fastapi import APIRouter, HTTPException, Request, Form
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from app.models import AIEnhanceRequest, AIPointsRequest
from app.utils.ai import enhance_resume_text, generate_experience_points
from typing import List

router = APIRouter(prefix="/api/ai")


@router.post("/enhance", response_class=JSONResponse)
async def enhance_with_ai(request: AIEnhanceRequest):
    """Enhance text with AI to make it more impactful and professional."""
    try:
        enhanced_text = await enhance_resume_text(request.text)
        return {"enhanced_text": enhanced_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI enhancement failed: {str(e)}")


@router.post("/generate-points", response_class=JSONResponse)
async def generate_points(request: AIPointsRequest):
    """Generate bullet points for a job position based on title and company."""
    try:
        points = await generate_experience_points(request.job_title, request.company)
        return {"points": points}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI point generation failed: {str(e)}")


@router.post("/generate-points-html", response_class=HTMLResponse)
async def generate_points_html(request: Request, job_title: str = Form(...), company: str = Form(...), exp_index: int = Form(...)):
    """Generate bullet points for a job position and return them as HTML."""
    try:
        templates = Jinja2Templates(directory="app/templates")
        points = await generate_experience_points(job_title, company)
        
        # Generate HTML for each point
        result_html = ""
        for i, point in enumerate(points):
            result_html += templates.get_template("components/point_item.html").render(
                request=request, point=point, exp_index=exp_index, point_index=f"new_{i}"
            )
        return result_html
    except Exception as e:
        return f"<div class='p-4 bg-red-100 text-red-800 rounded'>AI point generation failed: {str(e)}</div>"