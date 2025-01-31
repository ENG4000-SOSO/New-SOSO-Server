from fastapi import FastAPI
from app.views import example, auth

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "New SOSO Server!"}

# Include Additional Routers (Views)
app.include_router(example.router)
app.include_router(auth.router)
