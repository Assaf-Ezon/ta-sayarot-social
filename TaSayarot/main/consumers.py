from channels.generic.websocket import AsyncWebsocketConsumer
from TaSayarot.main.pages.main import Main
from TaSayarot.main.pages.forum import Forum
import json


class LikeConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("connection made")
        await self.accept()
        user = self.scope.get("user")
        if user.is_authenticated:
            print(str(user))

    async def disconnect(self, close_code):
        print(f"connection closed with code: {close_code}")

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        print(f"post id to like: {text_data_json}")

        user = self.scope.get("user")
        if user.is_authenticated:
            Main.submit_like(int(text_data_json['id']), str(user))


class ForumConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("connection made")
        await self.accept()
        user = self.scope.get("user")
        if user.is_authenticated:
            print(str(user))

    async def disconnect(self, close_code):
        print(f"connection closed with code: {close_code}")

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)

        user = self.scope.get("user")
        if user.is_authenticated:
            Forum.add_msg(str(user), text_data_json["forum_name"], text_data_json["messege"])

            await self.send(json.dumps({
                'user': str(user),
                'messege': text_data_json["messege"],
                'forum_name': text_data_json["forum_name"],
            }))
