from fastapi import APIRouter, Path
from celery.result import AsyncResult
from celery_tasks.celery import cel
import os
import shutil

feedback = APIRouter()


@feedback.get("/hello")
async def hello():
    return "fuck"


# 获取任务队列的执行情况
@feedback.get("/check/{task_id}")
async def check_task_id(task_id: str = Path(..., title="task id")):
    print("task_id is : ", task_id)
    async_result = AsyncResult(id=task_id, app=cel)
    data = ""
    if async_result.successful():
        code, msg, data = async_result.get()
    # result.forget() # 将结果删除,执行完成，结果不会自动删除
    # async.revoke(terminate=True)  # 无论现在是什么时候，都要终止
    # async.revoke(terminate=False) # 如果任务还没有开始执行呢，那么就可以终止。
    elif async_result.failed():
        code = 'FAILED'
        msg = '执行失败'
    elif async_result.status == 'PENDING':
        code = 'PENDING'
        msg = '任务等待中被执行'
    elif async_result.status == 'RETRY':
        code = 'RETRY'
        msg = '任务异常后正在重试'
    elif async_result.status == 'STARTED':
        code = 'STARTED'
        msg = '任务已经开始被执行'
    return {
        "code": code,
        "msg": msg,
        "data": data,
    }


# 删除用户模板
@feedback.get("/delete")
async def delete_user_template():
    try:
        # 先检查文件是否存在
        delete_path = "static/input/user/"
        print("delete_path:", delete_path)
        template_name = "user_template/"
        file_path = os.path.join(delete_path, template_name)
        if os.path.exists(file_path):  # 检查路径是否存在
            shutil.rmtree(file_path)
            print("文件夹删除成功")
        else:
            print("文件夹不存在")
    except Exception as e:
        # 返回失败的响应
        return {"code": "ERROR", "msg": str(e)}
    return {"code": "SUCCESS", "msg": "用户模板删除成功"}
