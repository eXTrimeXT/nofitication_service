import asyncio
from telegram import Bot
from ..config import TELEGRAM_BOT_TOKEN

class TelegramSender:
    @staticmethod
    def send(chat_id, message):
        try:
            bot = Bot(token=TELEGRAM_BOT_TOKEN)
            
            # Создаем event loop для синхронного вызова асинхронной функции
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            async def send_async():
                await bot.send_message(chat_id=chat_id, text=message)
            
            loop.run_until_complete(send_async())
            loop.close()
            return True
        except Exception as e:
            print(f"Ошибка отправки Telegram: {e}")
            return False