import fastapi from FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"Server running!"}
