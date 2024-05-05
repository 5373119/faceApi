from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from typing import Annotated
import uvicorn
import face_recognition
import shutil
import os

app = FastAPI()

# You can change this to any folder on your system
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


# 添加支持的图片类型
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.get("/")
async def root():
    return {"message": "caonima"}


#接收一个名为 file 的参数，该参数的类型是 UploadFile，
#我们使用 File 函数将其作为请求体中的文件进行解析。
# File 函数的第一个参数是文件类型的默认值，... 表示必须传递该参数，否则将会返回错误响应。
@app.post('/upload_image/')
async def upload_image(file: UploadFile = File(...)):
    # 检查文件格式是否正确
    if False == allowed_file(file.filename):
        print(f"upload filename is {file.filename}")
        return JSONResponse({"message": "File format is wrong"})
    #图片应该合格后再存储
    # 确保上传目录存在
    try:
        # 存储到指定的目录  返回值为空
        save_path = "E:\\test"
        save_name = "456" + ".png"
        print(os.makedirs(save_path, exist_ok=True))
        # 保存文件到服务器的指定目录并重命名
        file_path = os.path.join(save_path, save_name)
        print("file_path:", file_path)
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
    except Exception as e:
        # 返回失败的响应
        return JSONResponse({"error": str(e)}, status_code=500)
    # 返回一个响应
    return JSONResponse(content={"filename": save_name, "size": file.size})

    # # 检测图片是否上传成功
    # if 'file' not in request.files:
    #     return redirect(request.url)

    # file = request.files['file']

    # if file.filename == '':
    #     return redirect(request.url)

    # if file and allowed_file(file.filename):
    #     print(
    #         f"pony: **************** upload filename is {file.filename}******************"
    #     )
    #     # 图片上传成功，检测图片中的人脸
    #     return detect_faces_in_image(file)
    # return "jiuwfowwefoweo"
    # return {"filename": file.filename}
    # if file and allowed_file(file.filename):
    #     print(f"upload filename is {file.filename}")
    #     return JSONResponse({"message": "File uploaded successfully"})


def detect_faces_in_image(file_stream):

    # 载入用户上传的图片
    img = face_recognition.load_image_file(file_stream)

    shape = img.shape

    img_width = shape[0]

    img_height = shape[1]

    #图像宽度和高度
    print(f"pony: img.width is {img_width},height is {img_height}")

    #定位第一个人脸   这里要做异常校验

    face_locations = face_recognition.face_locations(img)

    print(f"pony: face_locations is  {face_locations}")

    if face_locations == []:

        print(f"pony: there is no face in the img")

        return "there is no face in the img"

    if len(face_locations) > 1:

        print(f"pony: there is more than one face in the img")

        return "there is more than one face in the img"

    face_width = face_locations[0][2] - face_locations[0][0]

    face_height = face_locations[0][1] - face_locations[0][3]

    print(f"pony: face_width is  {face_width},face_height is {face_height}")

    if face_width < img_width / 5 and face_height < img_height / 5:

        print(f"pony: face area is too small")

        return "face area is too small"

    face_landmarks_list = face_recognition.face_landmarks(
        img, face_locations=face_locations)

    print(f"pony: face_landmarks_list is \n {face_landmarks_list}")

    # 讲识别结果以json键值对的数据结构输出

    return jsonify(face_landmarks_list)


if __name__ == '__main__':
    uvicorn.run("face_detect:app", port=8080, reload=True)
