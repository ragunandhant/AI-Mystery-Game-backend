from fastapi import FastAPI
import router.user
from sql_app.database import engine
import sql_app.models as models
models.Base.metadata.create_all(bind=engine)
import router
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.include_router(router.user.router)

@app.get("/")
async def home():
    return {"message": "Hello, World!"}



