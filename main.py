from astrbot.api.star import Context, Star, register
from astrbot.api import logger
from aiohttp import web
import asyncio
import astrbot.api.message_components as Comp

routes = web.RouteTableDef()


@routes.post("/send")
async def handle_send(request):
    data = await request.json()
    umo = data.get("umo")
    message = data.get("message", "")
    at_user = data.get("at_user")

    if not umo or not message:
        return web.json_response({"error": "缺少 umo 或 message"}, status=400)

    chain = []
    if at_user:
        chain.append(Comp.At(qq=str(at_user)))
    chain.append(Comp.Plain(text=message))

    await handle_send._plugin.context.send_message(umo, chain)
    return web.json_response({"ok": True})


@register(
    "mention",
    "艾特/私聊消息发送",
    "提供HTTP API接口，支持艾特群成员或发送私聊消息",
    "1.0.0",
)
class MentionPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        handle_send._plugin = self

    async def initialize(self):
        app = web.Application()
        app.add_routes(routes)
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, "0.0.0.0", 8080)
        await site.start()
        logger.info("艾特插件已启动: http://0.0.0.0:8080/send")

    async def terminate(self):
        pass
