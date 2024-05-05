from fastapi import FastAPI, File, UploadFile
from typing import Annotated
import uvicorn

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "caonima"}


# 方法一：上传的文件会存在内存中，适合小型文件
@app.post("/")
async def create_file(file: Annotated[bytes | None, File()] = None):
    if not file:
        return {"message": "No file sent"}
    else:
        return {"file_size": len(file)}

if __name__ == '__main__':
    uvicorn.run("test-1:app", port=8080, reload=True)
