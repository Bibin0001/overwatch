import os
from dotenv import load_dotenv
from telethon import TelegramClient

load_dotenv()


class TelegramCollector:
	def __init__(self):
		self.api_id = int(os.environ["API_ID"])
		self.api_hash = os.environ["API_HASH"]
		self.client = TelegramClient("telegram_session", self.api_id, self.api_hash)


    async def start_client(self):
		await self.client.start()

	async def check_link(self, link):
		entity = await self.client.get_entity(link)
		links = []

		async for message in self.client.iter_messages(entity, limit=100):
			if message.message:
				links.append(f"{link.rstrip('/')}/{message.id}")

		return links

	async def close(self):
		await self.client.disconnect()

