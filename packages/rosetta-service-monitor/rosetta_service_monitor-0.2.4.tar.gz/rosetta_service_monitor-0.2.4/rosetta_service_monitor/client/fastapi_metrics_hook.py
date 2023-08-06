import time
import traceback
from typing import List

from loguru import logger

from rosetta_service_monitor.client.service.metrics_service import metrics_service
from fastapi import Response


def register_hook(app, project_name, scale: List[int] = None, **kwargs) -> None:
    """
    请求响应拦截fastapi请求上下文进行hook
    https://fastapi.tiangolo.com/tutorial/middleware/
    :param project_name:
    :param app:
    :param scale: stat scale.
    :return:
    """
    if not scale:
        scale = [i * 100 * 1000 for i in range(1, 21, 1)]
    @app.middleware("http")
    async def monitor(request, call_next):
        path = request.url.path.lstrip('/')
        response = None
        try:
            start = time.time()
            response: Response = await call_next(request)
        except KeyboardInterrupt:
            raise KeyboardInterrupt
        except Exception as err:
            info = f'{err}:{err.__class__.__name__}\n{traceback.format_exc()}'
            logger.error(info)
            defmodel = {
                "topic": "",
                "uri": path,
                "uri_tag": "s",
                "duration": int((time.time() - start) * 1e6),
                "code": response.status_code if response else 500,
                "isSuccess": "n",
                "scale": scale
            }
            metrics_service.send_async(defmodel=defmodel)
            raise err

        defmodel = {
            "topic": "",
            "uri": path,
            "uri_tag": "s",
            "duration": int((time.time() - start) * 1e6),
            "code": response.status_code,
            "isSuccess": "y",
            "scale": scale
        }

        metrics_service.send_async(defmodel=[defmodel])

        return response
