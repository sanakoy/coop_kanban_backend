from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from src.websocket.websocket import ws_manager


router = APIRouter()


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await ws_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Получено: {data}")

            await websocket.send_text(f"Echo: {data}")

            await ws_manager.broadcast(f"Broadcast: {data}")

    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)
        await ws_manager.broadcast("Клиент отключился")
    except Exception as e:
        print(f"Ошибка: {e}")
