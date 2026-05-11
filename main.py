from astrbot.api.star import Context, Star, register
from astrbot.api import logger


@register(
    "mention",
    "艾特/私聊消息发送",
    "提供HTTP API接口，支持艾特群成员或发送私聊消息",
    "1.0.0",
)
class MentionPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        # 注册 Web API
        context.register_web_api(
            "/mention/send",
            self.handle_send,
            ["POST"],
            "发送艾特或私聊消息",
        )

    async def handle_send(self):
        """处理发送消息的 HTTP API 请求"""
        from quart import request
        import astrbot.api.message_components as Comp

        try:
            data = await request.get_json()
            umo = data.get("umo")
            message = data.get("message", "")
            at_user = data.get("at_user")

            if not umo:
                return {"status": "error", "message": "缺少 umo 参数"}, 400
            if not message:
                return {"status": "error", "message": "缺少 message 参数"}, 400

            # 构建消息链
            chain = []
            if at_user:
                chain.append(Comp.At(qq=str(at_user)))
            chain.append(Comp.Plain(text=message))

            # 发送消息
            await self.context.send_message(umo, chain)

            return {"status": "ok", "message": "消息已发送", "data": {"umo": umo}}
        except Exception as e:
            logger.exception("发送消息失败")
            return {"status": "error", "message": str(e)}, 500

    async def terminate(self):
        pass
