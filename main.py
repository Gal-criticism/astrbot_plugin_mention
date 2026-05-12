from astrbot.api.star import Context, Star, register
from astrbot.api import logger
from astrbot.core.message.message_event_result import MessageChain
import astrbot.api.message_components as Comp
from quart import request, jsonify


@register(
    "astrbot_plugin_mention",
    "艾特/私聊消息发送",
    "提供HTTP API接口，支持艾特群成员或发送私聊消息",
    "1.0.0",
)
class MentionPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        self.context.register_web_api(
            "/astrbot-plugin-mention/send",
            self.handle_send,
            ["POST"],
            "发送艾特消息",
        )

    async def handle_send(self):
        try:
            data = await request.get_json()
            umo = data.get("umo")
            message = data.get("message", "")
            at_user = data.get("at_user")

            if not umo or not message:
                return jsonify({"error": "缺少 umo 或 message"}), 400

            chain = MessageChain(chain=[])
            if at_user:
                chain.at(qq=str(at_user))
            chain.message(message=message)

            # 包装成 MessageChain
            await self.context.send_message(umo, chain)
            return jsonify({"ok": True})
        except Exception as e:
            logger.error(f"发送消息失败: {e}")
            return jsonify({"error": str(e)}), 500

    async def initialize(self):
        logger.info(
            "艾特插件 Web API 已注册: POST /api/plug/astrbot-plugin-mention/send"
        )

    async def terminate(self):
        pass
