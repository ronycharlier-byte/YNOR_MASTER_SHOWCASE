from fastapi import FastAPI
import os

app = FastAPI(title="MDL Ynor Rescue Mode V11.9.8")

@app.get("/")
async def root():
    return {
        "status": "RESCUE_MODE", 
        "message": "Le noyau minimaliste est en ligne. L'API est vivante.",
        "env": os.getenv("PORT", "NOT_SET")
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
