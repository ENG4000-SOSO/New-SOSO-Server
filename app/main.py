from fastapi import FastAPI
from app.views import auth, users, admin, assets

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "New SOSO Server!"}

# Include Additional Routers (Views)
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(admin.router)
app.include_router(assets.router)
