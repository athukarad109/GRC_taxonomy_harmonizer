from fastapi import FastAPI
from api.routes import router

app = FastAPI(title="Control Harmonization Engine")

# Register routes
app.include_router(router)
