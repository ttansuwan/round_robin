from fastapi import FastAPI, Request

app = FastAPI()

@app.post("/")
async def root(request: Request):
    # Return payload immediately
    return await request.json()