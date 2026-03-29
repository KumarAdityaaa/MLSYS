from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from routes.chat import router as chat_router
from routes.data import router as data_router
from routes.eda import router as eda_router
from routes.experiments import router as exp_router
from routes.memory import router as memory_router
from routes.research import router as research_router

app = FastAPI()

# Middleware BEFORE routers
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="."), name="static")

app.include_router(memory_router)
app.include_router(eda_router)
app.include_router(chat_router)
app.include_router(exp_router)
app.include_router(data_router)
app.include_router(research_router)

@app.get("/")
def root():
    return {"message": "ML AI System Running 🚀"}
