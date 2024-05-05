from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from typing import Annotated
import uvicorn
import face_recognition
import json
import os

app = FastAPI()

# You can change this to any folder on your system
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


# 添加支持的图片类型
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.get("/", summary="仅测试用接口")
async def root():
    return {"message": "caonima"}


#接收一个名为 file 的参数，该参数的类型是 UploadFile，
#我们使用 File 函数将其作为请求体中的文件进行解析。
# File 函数的第一个参数是文件类型的默认值，... 表示必须传递该参数，否则将会返回错误响应。
@app.post('/upload_image/', summary="图像上传接口")
async def upload_image(file: UploadFile = File(...)):
    # 先检查文件格式是否正确
    if False == allowed_file(file.filename):
        return JSONResponse({"code": "Error", "msg": "File format is wrong"})
    #图片应该合格后再存储
    # 确保上传目录存在
    try:
        # 存储到指定的目录  返回值为空
        save_path = "E:\\test"
        save_name = "789" + ".png"
        print(os.makedirs(save_path, exist_ok=True))
        # 保存文件到服务器的指定目录并重命名
        file_path = os.path.join(save_path, save_name)
        print("file_path:", file_path)
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
    except Exception as e:
        # 返回失败的响应
        return JSONResponse({"code": "Error", "msg": str(e)})
    #这个时候文件还没读取
    code, msg = detect_faces_in_image(file_path)
    if code == "Error":
        try:
            os.remove(file_path)
            print(f"文件 {file_path} 已被删除。")
        except OSError as e:
            print(f"无法删除文件: {e}")
        finally:
            return JSONResponse({"code": "Error", "msg": msg})
    return JSONResponse({"code": code, "msg": msg})


# 人脸图片检测
def detect_faces_in_image(file_stream):
    # 载入用户上传的图片
    img = face_recognition.load_image_file(file_stream)
    shape = img.shape
    img_width = shape[0]
    img_height = shape[1]

    #图像宽度和高度
    print(f"img.width is {img_width},height is {img_height}")
    #定位第一个人脸  这里要做异常校验
    face_locations = face_recognition.face_locations(img)
    print(f"face_locations is  {face_locations}")
    if face_locations == []:
        return "Error", "未在图片中检测到人脸"

    if len(face_locations) > 1:
        return "Error", "在图片中检测到多个人脸"
    # 第一个人脸矩形的宽和高
    face_width = face_locations[0][2] - face_locations[0][0]
    face_height = face_locations[0][1] - face_locations[0][3]
    print(f"face_width is  {face_width},face_height is {face_height}")
    # 人脸在图像中占比
    if face_width < img_width / 5 and face_height < img_height / 5:
        return "Error", "人脸在图像中占比过小"
    # 检测人脸五官
    face_landmarks_list = face_recognition.face_landmarks(
        img, face_locations=face_locations)
    print(f"face_landmarks_list is \n {face_landmarks_list}")
    # 将识别结果以json键值对的数据结构输出
    # 使用json.loads()方法将字符串转换为字典
    return "Success", "图片合格"


if __name__ == '__main__':
    uvicorn.run("face_detect:app", port=8080, reload=True)
