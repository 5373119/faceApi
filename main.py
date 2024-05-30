from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn
from apps.app_mini.urls import detect
from apps.app_cloud.urls import feedback

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(detect,prefix="/detect",tags=["小程序请求接口"])
app.include_router(feedback,prefix="/feedback",tags=["云端请求接口"])


if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0",port=8080, reload=True)
