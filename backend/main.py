from fastapi import FastAPI
from pydantic import BaseModel
import cohere
from typing import Dict
import dotenv 
import os 
dotenv.load_dotenv()

# cohere api key variable 
cohere_api=os.environ.get("cohere_api_key")

# Initialize FastAPI app
app = FastAPI()

# Cohere API Key setup
cohere_client = cohere.Client(cohere_api)  # Replace with your Cohere API Key

# Business Idea Model for Request
class BusinessIdea(BaseModel):
    idea: str

# Cohere analysis function
def analyze_business_idea(idea: str) -> str:
    # Multi-step prompts to Cohere API for a detailed analysis
    prompt = f""" You are an expert business consultant. A student has presented the following business idea: "{idea}."

        Please provide a concise, yet comprehensive analysis, focusing on:

        Feasibility: Clearly explain whether this idea is practical from both a technical and economic perspective. Highlight key barriers and opportunities.
        Sustainability: Summarize its environmental and social impact, and note how it aligns with or violates key sustainability goals (SDGs).
        Market Cap: Provide a specific market estimate, along with key factors influencing market growth.
        Uniqueness: Identify what makes this idea different from competitors and how well it stands out.
        Impact: Focus on the tangible social, environmental, or economic impact the idea can achieve.
        Risks: List the primary risks (internal and external) and weaknesses that could affect the success of this idea.
        Improvements: Suggest three specific, actionable improvements.
         Additionally, please rate the following on a scale of 1-10:

        Feasibility
        Uniqueness
        Impact
        Market Cap potential
        Sustainability"""

    # Request to Cohere API for analysis
    response = cohere_client.generate(
        model="command-light",  # Specify the model size
        prompt=prompt,
        max_tokens=12000
    )

    # Return the text of the response
    return response.generations[0].text.strip()

# Endpoint to evaluate the business idea
@app.post("/evaluate/")
def evaluate_idea(business_idea: BusinessIdea) -> Dict[str, str]:
    feedback = analyze_business_idea(business_idea.idea)
    return {"feedback": feedback}

# Run the application using uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
