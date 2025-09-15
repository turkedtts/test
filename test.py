from .. import loader, utils
import asyncio

@loader.tds
class AutoSenderMod(loader.Module):
    """Автоотправка текста в чат каждые 3.5 секунды"""
    strings = {"name": "AutoSender"}

    def init(self):
        self.db = {}   # чтобы не было ошибки
        self._running = False

    @loader.command()
    async def getid(self, message):
        """Получить ID текущего чата"""
        await message.edit(f"ID этого чата: {message.chat_id}")

    @loader.command()
    async def setid(self, message):
        """Установить ID чата: .setid <id>"""
        args = utils.get_args_raw(message)
        if not args:
            # Если аргументов нет — берем id текущего чата
            chat_id = message.chat_id
        else:
            chat_id = int(args)

        self.set("chat_id", chat_id)
        await message.edit(f"ID чата установлен: {chat_id}")

    @loader.command()
    async def settext(self, message):
        """Установить текст: .settext <текст>"""
        args = utils.get_args_raw(message)
        if not args:
            return await message.edit("Укажи текст")
        self.set("text", args)
        await message.edit(f"Текст установлен: {args}")

    @loader.command()
    async def startspam(self, message):
        """Запустить рассылку"""
        if self._running:
            return await message.edit("Уже работает")

        chat_id = self.get("chat_id", None)
        text = self.get("text", None)

        if not chat_id:
            return await message.edit("Сначала установи ID чата (.setid)")
        if not text:
            return await message.edit("Сначала установи текст (.settext)")

        await message.edit("Запускаю рассылку...")
        self._running = True

        try:
            while self._running:
                await self.client.send_message(chat_id, text)
                await asyncio.sleep(3.5)
        except Exception as e:
            await message.respond(f"Ошибка: {e}")
        finally:
            self._running = False

    @loader.command()
    async def stopspam(self, message):
        """Остановить рассылку"""
        if not self._running:
            return await message.edit("Не запущено")
        self._running = False
        await message.edit("Рассылка остановлена")
