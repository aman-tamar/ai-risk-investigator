from fastapi import FastAPI

app = FastAPI(
    title="AI Risk Investigator",
    description="AI-powered financial transaction risk investigation system",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "ai-risk-investigator",
    }