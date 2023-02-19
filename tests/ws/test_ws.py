import pytest
from starlette.testclient import WebSocketTestSession, TestClient

from main import app
from mock import CombotUserDBGenerator
from settings import settings
from telegram.communication_bot.combot_deps import broadcast
from telegram.communication_bot.combot_utils import get_ws_room_name


@pytest.mark.asyncio
@pytest.mark.skip('Виснет почему то')
async def test_websocket():
    client = TestClient(app)
    generator = CombotUserDBGenerator()
    await generator.generate_mock_data()
    with client.websocket_connect(f'{settings.PROXY_PREFIX}/ws/1') as ws:
        ws: WebSocketTestSession
        print('PRIVET')
        text = ws.receive_text()
        print(text)
        ws.send_text('TEXT')
        ws.send_text('NOT TEXT')

        print('POKA')
    print('ZDAROVA')
        # print(broadcast._subscribers)
    # async with broadcast.subscribe(channel=get_ws_room_name(1)) as subscriber:
