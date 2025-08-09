from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from src.api.v1 import task_http, websocket
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(default_response_class=ORJSONResponse)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(task_http.router, prefix="/kanban/api/v1/task", tags=["task"])
app.include_router(websocket.router, prefix="", tags=["websocket"])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
