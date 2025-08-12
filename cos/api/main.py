from fastapi import FastAPI

app = FastAPI(title="CoS Control Plane")

@app.get("/health")
def health():
    return {"status": "ok"}
