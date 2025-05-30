import discord
import asyncio
import os

# กำหนด Channel IDs
VOICE_CHANNEL_ID = 1375227595741855825
TEXT_CHANNEL_ID = 1375767832234823740

# อ่าน Environment Variable ชื่อ BOT_TOKENS แล้วแยกด้วยเครื่องหมายคอมมา
BOT_TOKENS = os.getenv("BOT_TOKENS", "").split(",")

class VoiceBot(discord.Client):
    def __init__(self, token):
        super().__init__(intents=discord.Intents.all())
        self.token = token
        self.voice_client = None

    async def on_ready(self):
        print(f"[{self.user}] บอทออนไลน์เรียบร้อย")
        await asyncio.gather(
            self.join_voice_loop(),
            self.send_status_loop()
        )

    async def join_voice_loop(self):
        await self.wait_until_ready()
        while not self.is_closed():
            try:
                channel = self.get_channel(VOICE_CHANNEL_ID)
                if channel and isinstance(channel, discord.VoiceChannel):
                    if not self.voice_client or not self.voice_client.is_connected():
                        self.voice_client = await channel.connect()
                        print(f"[{self.user}] เข้าห้องเสียงแล้ว")
                await asyncio.sleep(10)
            except Exception as e:
                print(f"[{self.user}] voice error: {e}")
                await asyncio.sleep(10)

    async def send_status_loop(self):
        await self.wait_until_ready()
        while not self.is_closed():
            try:
                channel = self.get_channel(TEXT_CHANNEL_ID)
                if channel and isinstance(channel, discord.TextChannel):
                    await channel.send(f"✅ [{self.user}] ยังออนไลน์อยู่และอยู่ในห้องเสียงเรียบร้อย")
                    print(f"[{self.user}] ส่งข้อความสถานะแล้ว")
                await asyncio.sleep(3600)  # ส่งทุก 1 ชั่วโมง
            except Exception as e:
                print(f"[{self.user}] message error: {e}")
                await asyncio.sleep(60)

async def run_all_bots():
    tasks = []
    for token in BOT_TOKENS:
        token = token.strip()
        if token:
            bot = VoiceBot(token)
            tasks.append(bot.start(token))
    await asyncio.gather(*tasks)

# เริ่มรันทุกบอท
asyncio.run(run_all_bots())
