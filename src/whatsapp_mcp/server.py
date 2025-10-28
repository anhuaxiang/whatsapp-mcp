
import os
import httpx
from pydantic import Field, BaseModel
from mcp.server.fastmcp import FastMCP
from typing import List, Optional, Annotated, Literal, Union
import logging

VERSION = "v22.0"
PHONE_NUMBER_ID = os.environ["PHONE_NUMBER_ID"]
ACCESS_TOKEN = os.environ["ACCESS_TOKEN"]
BUSINESS_ACCOUNT_ID = os.environ['BUSINESS_ACCOUNT_ID']

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
}

mcp = FastMCP("whatsapp-mcp")


# lark机器人发送单聊消息
@mcp.tool(description="Send a plain text message to a WhatsApp user via the WhatsApp Business Cloud API.")
async def send_text_message(
        to: Annotated[str, Field(description="Recipient's WhatsApp number in international format")],
        text: Annotated[str, Field(description="Text message content")],
) -> dict:
    url = f"https://graph.facebook.com/{VERSION}/{PHONE_NUMBER_ID}/messages"
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": text},
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)
    return response.json()


@mcp.tool(description="List all approved or pending WhatsApp message templates under the connected Business Account (WABA).")
async def list_template(
    limit: Annotated[int, Field(description="Number of templates to retrieve")] = 20,
    after: Annotated[Optional[str], Field(description="Cursor for pagination")] = None,
) -> dict:
    url = f"https://graph.facebook.com/{VERSION}/{BUSINESS_ACCOUNT_ID}/message_templates"
    params = {"limit": limit}
    if after:
        params["after"] = after

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params, headers=headers)
    return response.json()





@mcp.tool(description="Send a pre-approved WhatsApp message template with optional parameters and language code.")
async def send_template_message(
        to: Annotated[str, Field(description="Recipient's WhatsApp number in international format")],
        template_name: Annotated[str, Field(description="Template name")],
        language_code: Annotated[str, Field(description="Language code, e.g., en_US")] = "en_US",
        parameters: Annotated[Optional[List[str]], Field(description="List of template parameters")] = None,
) -> dict:
    url = f"https://graph.facebook.com/{VERSION}/{PHONE_NUMBER_ID}/messages"
    template_payload = {
        "name": template_name,
        "language": {"code": language_code},
    }
    if parameters:
        template_payload["components"] = [{
            "type": "body",
            "parameters": [{"type": "text", "text": param} for param in parameters]
        }]
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "template",
        "template": template_payload,
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)
    return response.json()


def main():
    mcp.run()


if __name__ == '__main__':
    main()
