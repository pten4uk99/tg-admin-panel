import os
import sys
from pathlib import Path

import uvicorn


sys.path.append(os.path.join(Path(__file__).resolve().parent, 'src'))

from fastapi import FastAPI, WebSocketException, WebSocket
from fastapi.responses import HTMLResponse
from tortoise.contrib.fastapi import register_tortoise

from src.telegram.communication_bot.combot_services import chatroom_ws_sender, find_chat_by_user_id
from src.settings import settings
from src.admin.auth.auth_app import auth_router
from src.telegram.communication_bot import combot_app


app = FastAPI(
    title='TG REST SERVICE',
)
app.include_router(combot_app.combot_router, prefix=settings.PROXY_PREFIX)
app.include_router(auth_router, prefix=settings.PROXY_PREFIX)


html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws/1");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


# @app.get("/")
# async def get():
#     return HTMLResponse(html)


@app.on_event('startup')
async def on_startup():
    print('APP STARTUP')

    register_tortoise(
        app,
        db_url=settings.DATABASE_URL,
        generate_schemas=True,
        add_exception_handlers=False,
        modules={
            'models': [
                'telegram.communication_bot.combot_dao',
                'admin.auth.auth_dao',
            ]
        },
    )


@app.on_event('shutdown')
async def on_shutdown():
    print('APP SHUTDOWN')


@app.websocket('/api/ws/{user_id}')
async def chatroom_ws(user_id: int, websocket: WebSocket):
    chat = await find_chat_by_user_id(user_id)

    if not chat:
        raise WebSocketException(
            reason='Чата пользователя не существует в БД',
            code=400
        )

    await websocket.accept()
    await websocket.send_text('Success connection')
    await chatroom_ws_sender(websocket, chat_id=chat.id)


@app.get('/metrics')
async def metrics():
    return 200


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
        reload=False,
    )
