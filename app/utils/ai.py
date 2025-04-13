from typing import List
from litellm import completion
from app.config import get_model_config

# Get model configuration
model_config = get_model_config()
DEFAULT_MODEL = model_config["model"]

async def get_completion(
    prompt: str, 
    system_prompt: str = None,
    temperature: float = 0.7,
    max_tokens: int = 500
) -> str:
    """
    Get a completion from LiteLLM using the configured model.
    """
    messages = []
    
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    
    messages.append({"role": "user", "content": prompt})
    
    try:
        response = completion(
            model=DEFAULT_MODEL,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error getting AI completion: {e}")
        return f"AI generation failed. Please try again later. Error: {str(e)}"

async def enhance_resume_text(text: str) -> str:
    """
    Enhance a resume text to make it more impactful and professional.
    """
    system_prompt = """
    You are an expert resume writer. Your task is to enhance the given text to make it more
    impactful, professional, and results-oriented for a resume.
    
    Guidelines:
    - Use strong action verbs
    - Include metrics and quantifiable achievements where possible
    - Be concise but comprehensive
    - Maintain the core meaning and facts
    - Avoid generic language and clichés
    - Ensure the text is in past tense for past roles
    - Focus on achievements rather than responsibilities
    """
    
    prompt = f"""
    Please enhance the following resume text to make it more impactful and professional:
    
    "{text}"
    
    Provide only the enhanced text without explanations or additional formatting.
    """
    
    return await get_completion(prompt, system_prompt, temperature=0.6)


async def generate_experience_points(job_title: str, company: str) -> List[str]:
    """
    Generate bullet points for a job position based on title and company.
    """
    system_prompt = """
    You are an expert resume writer. Your task is to generate impressive, achievement-oriented
    bullet points for a resume based on a job title and company.
    
    Guidelines:
    - Create 3 bullet points that highlight achievements, not just responsibilities
    - Include metrics and quantifiable results (use realistic percentages and numbers)
    - Use strong action verbs at the beginning of each point
    - Be specific and relevant to the job title
    - Ensure points are concise but detailed enough to be impactful
    - Format in past tense for maximum impact
    """
    
    prompt = f"""
    Generate 3 impressive bullet points for a resume for the position of "{job_title}" at "{company}".
    Each bullet point should start with a strong action verb, include metrics, and be specific to the role.
    Format the response as a simple list without numbering, bullet points, or quotes.
    """
    
    response = await get_completion(prompt, system_prompt, temperature=0.7, max_tokens=800)
    
    # Process the response to get a clean list of points
    points = [line.strip() for line in response.strip().split('\n') if line.strip()]
    # Clean up any remaining bullets or numbers
    points = [p[2:].strip() if p.startswith('- ') else p for p in points]
    points = [p[3:].strip() if p[0].isdigit() and p[1:3] in ['. ', ') '] else p for p in points]
    
    return points[:3]  # Ensure we return exactly 3 points
