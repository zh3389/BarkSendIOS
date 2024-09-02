from fastapi import FastAPI
from pydantic import BaseModel, Field
from BarkNotificator import BarkNotificator
import config

"""关闭 422 错误"""
_openapi = FastAPI.openapi


def openapi(self: FastAPI):
    _openapi(self)

    for _, method_item in self.openapi_schema.get('paths').items():
        for _, param in method_item.items():
            responses = param.get('responses')
            # remove 422 response, also can remove other status code
            if '422' in responses:
                del responses['422']

    return self.openapi_schema


FastAPI.openapi = openapi

"""正式的应用程序开始行"""
app = FastAPI(title="Bark API",
              description="这是一个 Bark API 发送消息到 IOS 系统的示例",
              version="0.1.0",
              contact={"name": "zh API",
                       "url": "http://192.168.101.118:20002/docs",
                       "email": "zhanghao_3389@163.com",
                       },
              license_info={"name": "Apache 2.0",
                            "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
                            },
              redoc_url=None
              )


class InputData(BaseModel):
    title: str = Field("welcome", description="标题")
    content: str = Field("hello world", description="内容")


class OutputData(BaseModel):
    success: bool = Field(True, description="请求是否成功")
    code: int = Field(200, description="响应状态码")
    data: str = Field("title: welcome, content: hello world", description="数据")
    msg: str = Field("发送成功", description="响应信息")


@app.post("/api/v1/bark/send", response_model=OutputData, summary="Bark消息传送")
async def process_data(cla: InputData):
    """
    此接口通过向接口发送消息，Bark 服务转发给 IOS 系统。
    """
    try:
        bark = BarkNotificator(device_token=config.device_token)
        bark.send(title=cla.title, content=cla.content)
        return OutputData(success=True, code=200, data=f"title: {cla.title}, content: {cla.content}", msg="发送成功")
    except Exception as e:
        return OutputData(success=False, code=500, data=f"title: {cla.title}, content: {cla.content}", msg="发送失败, 错误信息: " + str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
