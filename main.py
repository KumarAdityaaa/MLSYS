from fastapi import FastAPI
from routes.chat import router as chat_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.chat import router as chat_router
from fastapi.staticfiles import StaticFiles
from routes.data import router as data_router
from routes.eda import router as eda_router
from routes.experiments import router as exp_router
from routes.memory import router as memory_router

app = FastAPI()

app.mount("/static", StaticFiles(directory="."), name="static")
app.include_router(memory_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(eda_router)
app.include_router(chat_router)
app.include_router(exp_router)
app.include_router(data_router)
@app.get("/")
def root():
    return {"message": "ML AI System Running 🚀"}