from .. import loader, utils
import asyncio

@loader.tds
class AutoSenderMod(loader.Module):
    """Автоотправка текста в чат каждые 3.5 секунды"""
    strings = {"name": "AutoSender"}

    def init(self):
        self.config = loader.ModuleConfig(
            "chat_id", None, "ID чата для отправки",
            "text", "Привет!", "Текст для отправки"
        )
        self._running = False

    @loader.command()
    async def getid(self, message):
        """Получить ID текущего чата"""
        await message.edit(f"ID этого чата: {message.chat_id}")

    @loader.command()
    async def setid(self, message):
        """Установить ID чата для рассылки: .setid <id>"""
        args = utils.get_args_raw(message)
        if not args:
            return await message.edit("Укажи ID чата")
        self.config["chat_id"] = int(args)
        await message.edit(f"ID чата установлен: {args}")

    @loader.command()
    async def settext(self, message):
        """Установить текст для рассылки: .settext <текст>"""
        args = utils.get_args_raw(message)
        if not args:
            return await message.edit("Укажи текст")
        self.config["text"] = args
        await message.edit(f"Текст установлен: {args}")

    @loader.command()
    async def startspam(self, message):
        """Запустить рассылку"""
        if self._running:
            return await message.edit("Уже работает")
        chat_id = self.config["chat_id"]
        if not chat_id:
            return await message.edit("Сначала установи ID чата")
        text = self.config["text"]

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
