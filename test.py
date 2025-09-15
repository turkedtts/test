from .. import loader, utils
from asyncio import sleep


def register(cb):
    cb(AutoSenderMod())


class AutoSenderMod(loader.Module):
    """Автоотправка текста в чат каждые 3.5 сек"""

    strings = {"name": "AutoSender"}

    def __init__(self):
        self._running = False
        self._chat_id = None
        self._text = None

    async def getidcmd(self, message):
        """Показать ID текущего чата"""
        await message.edit(f"ID этого чата: `{message.chat_id}`")

    async def setidcmd(self, message):
        """Установить ID чата (.setid <id> или без аргументов — текущий чат)"""
        args = utils.get_args_raw(message)
        if args:
            self._chat_id = int(args)
        else:
            self._chat_id = message.chat_id
        await message.edit(f"ID чата установлен: `{self._chat_id}`")

    async def settextcmd(self, message):
        """Установить текст (.settext <текст>)"""
        args = utils.get_args_raw(message)
        if not args:
            return await message.edit("Укажи текст")
        self._text = args
        await message.edit(f"Текст установлен: {self._text}")

    async def startspamcmd(self, message):
        """Запустить автоотправку"""
        if self._running:
            return await message.edit("Уже работает")
        if not self._chat_id:
            return await message.edit("Сначала установи ID чата (.setid)")
        if not self._text:
            return await message.edit("Сначала установи текст (.settext)")

        await message.edit("Запускаю рассылку...")
        self._running = True

        try:
            while self._running:
                await message.client.send_message(self._chat_id, self._text)
                await sleep(3.5)
        except Exception as e:
            await message.respond(f"Ошибка: {e}")
        finally:
            self._running = False

    async def stopspamcmd(self, message):
        """Остановить автоотправку"""
        if not self._running:
            return await message.edit("Не запущено")
        self._running = False
        await message.edit("Рассылка остановлена")

    async def showspamcmd(self, message):
        """Показать текущие настройки"""
        chat_id = self._chat_id or "не задан"
        text = self._text or "не задан"
        await message.edit(f"📌 Чат: `{chat_id}`\n📌 Текст: {text}")
