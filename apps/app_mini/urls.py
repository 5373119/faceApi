from fastapi import File, UploadFile, APIRouter
from fastapi.responses import JSONResponse
import os
from celery_tasks.task_detect import detect_face
import random
import string

detect = APIRouter()

# 生成随机字符串
def generate_random_string(length=16):
    # 字符集包括小写字母和数字
    chars = string.ascii_lowercase + string.digits
    return ''.join(random.choices(chars, k=length))

# You can change this to any folder on your system
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


# 添加支持的图片类型
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@detect.get("/hello", summary="仅测试用接口")
async def hello():
    return "fuck"


#接收一个名为 file 的参数，该参数的类型是 UploadFile，
#我们使用 File 函数将其作为请求体中的文件进行解析。
# File 函数的第一个参数是文件类型的默认值，... 表示必须传递该参数，否则将会返回错误响应。
@detect.post('/add', summary="图像上传接口")
async def upload_image(file: UploadFile = File(...)):
    print("file.filename:",file.filename)
    # 先检查文件格式是否正确
    if False == allowed_file(file.filename):
        return {"code": "Error", "msg": "File format is wrong"}
    #图片应该合格后再存储
    # 确保上传目录存在
    try:
        # 存储到指定的目录  返回值为空
        # random_path = generate_random_string(16)
        # print("random_path:",random_path)
        save_path = "E:\\test\\user_template\\"
        print("save_path:",save_path)
        save_name = "0.png"
        print(os.makedirs(save_path, exist_ok=True))
        # 保存文件到服务器的指定目录并重命名
        file_path = os.path.join(save_path, save_name)
        print("file_path:", file_path)
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
    except Exception as e:
        # 返回失败的响应
        return {"code": "Error", "msg": str(e)}
    # 立即告知celery去执行celery任务，并传入一个参数
    result = detect_face.delay(file_path)
    print("result: ",result)
    return {"code":"SUCCESS","data":result.id}





