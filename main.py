from functools import lru_cache
from fastapi import Depends, FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import ORJSONResponse
from src.api.v1 import task_http
from src.db.postgres import get_session
from src.services.task_service import TaskService
from src.api.v1.task_ws import manager
from sqlalchemy.ext.asyncio import AsyncSession

app = FastAPI(default_response_class=ORJSONResponse)


@app.get("/")
def read_root():
    return {"message": "HTTP работает"}


app.include_router(task_http.router, prefix="/kanban/api/v1", tags=["task"])


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()  # Получаем сообщение
            print(f"Получено: {data}")  # Логируем на сервере

            # Отправляем ответ
            await websocket.send_text(f"Echo: {data}")

            # Или рассылаем всем (broadcast)
            await manager.broadcast(f"Broadcast: {data}")

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast("Клиент отключился")
    except Exception as e:
        print(f"Ошибка: {e}")


@lru_cache()
def get_task_service(
    session: AsyncSession = Depends(get_session),
) -> TaskService:
    return TaskService(session, manager)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
