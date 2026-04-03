from fastapi import FastAPI
import os

# MDL YNOR ELITE V11.12.0 - IRON CORE (HYPER-LIGHT)
# ZÉRO IMPORT LOURD - ZÉRO DONNÉE - TEST DE VIE PUR mu=1.0

app = FastAPI(title="MDL YNOR IRON CORE")

@app.get("/")
async def root():
    return {"status": "LIVE", "mu": 1.0, "message": "Iron Core Active. The Empire is breathing."}

@app.get("/health")
async def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
