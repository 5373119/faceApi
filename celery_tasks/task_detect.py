from celery_tasks.celery import cel
import face_recognition
import os

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
        return "ERROR", "未在图片中检测到人脸"

    if len(face_locations) > 1:
        return "ERROR", "在图片中检测到多个人脸"
    # 第一个人脸矩形的宽和高
    face_width = face_locations[0][2] - face_locations[0][0]
    face_height = face_locations[0][1] - face_locations[0][3]
    print(f"face_width is  {face_width},face_height is {face_height}")
    # 人脸在图像中占比
    if face_width < img_width / 5 and face_height < img_height / 5:
        return "ERROR", "人脸在图像中占比过小"
    # 检测人脸五官
    face_landmarks_list = face_recognition.face_landmarks(
        img, face_locations=face_locations)
    print(f"face_landmarks_list is \n {face_landmarks_list}")
    # 将识别结果以json键值对的数据结构输出
    # 使用json.loads()方法将字符串转换为字典
    return "SUCCESS", "图片合格"



@cel.task
def detect_face(file_path):
    code, msg = detect_faces_in_image(file_path)
    if code == "ERROR":
        try:
            os.remove(file_path)
            print(f"文件 {file_path} 已被删除。")
        except OSError as e:
            print(f"无法删除文件: {e}")
        finally:
            return code,msg,""
    # 如果成功，则返回存储路径    
    return code,msg,file_path

