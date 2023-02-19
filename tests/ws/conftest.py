import pytest

from starlette.testclient import WebSocketTestSession, TestClient

from main import app


# @pytest.fixture
# def ws():
#     client = TestClient(app)
#
#     with client.websocket_connect('/ws/1') as ws:
#         ws: WebSocketTestSession
#         yield ws
#         ws.close()
