from fastapi import FastAPI

app = FastAPI(title="PayLink")


@app.get("/health")
def health():
    return {"status": "ok"}
