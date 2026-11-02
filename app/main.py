from app.routers.routes import router
from fastapi import FastAPI
from app.db.database import engine,base
from fastapi.middleware.cors import CORSMiddleware

base.metadata.create_all(bind=engine)

app = FastAPI(title="check that out")

origins = ["*"]

app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_headers=["*"], allow_methods=["*"])

app.include_router(router=router)

@app.post('/')
def root():
    return {
        "message" : "successful"
    }