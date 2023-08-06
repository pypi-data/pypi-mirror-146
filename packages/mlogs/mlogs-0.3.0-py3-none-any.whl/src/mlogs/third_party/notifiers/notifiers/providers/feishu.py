from ..core import Provider
from ..core import Response
from ..utils import requests


class Feishu(Provider):
    """Send Feishu webhook notifications"""
    base_url = "https://www.feishu.cn/hc/zh-CN/articles/360040566333"
    site_url = "https://open.feishu.cn/document/home/index"
    name = "feishu"

    __attachments = {
        # "additionalProperties": False,
    }
    _required = {"required": ["webhook_url", "message"]}
    _schema = {
        "type": "object",
        "properties": {
            "webhook_url": {
                "type": "string",
                "format": "uri",
                "title": "the webhook URL to use. Register one at https://my.slack.com/services/new/incoming-webhook/",
            },
            "username": {"type": "string", "title": "override the displayed bot name"},
            "msg_type": {
                "type": "string",
                "title": "this is msg_type like text, more text ..."
            },
            "message": {"type": "string", "title": "the content of the email message"},
            "content": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "text": {"type": "string"},
                },
            },
            "attachments": __attachments,
        }
    }

    def _prepare_data(self, data: dict) -> dict:
        data["content"]["text"] = data.pop("message")
        return data

    def _send_notification(self, data: dict) -> Response:
        url = data.pop("webhook_url")
        response, errors = requests.post(url, json=data)
        return self.create_response(data, response, errors)
