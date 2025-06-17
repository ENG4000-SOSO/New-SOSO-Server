import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.views import \
    admin, \
    auth, \
    assets, \
    imaging, \
    maintenance, \
    mission, \
    outage, \
    schedule, \
    users


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "New SOSO Server!"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# Include Additional Routers (Views)
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(admin.router)
app.include_router(assets.router)
app.include_router(maintenance.router)
app.include_router(imaging.router)
app.include_router(outage.router)
app.include_router(mission.router)
app.include_router(schedule.router)
