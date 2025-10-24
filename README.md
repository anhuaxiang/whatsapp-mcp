# WhatsApp MCP

A Model Context Protocol (MCP) server for WhatsApp.


```json

{
  "mcpServers": {
    "whatsapp-mcp": {
      "env": {
        "ACCESS_TOKEN": "ACCESS_TOKEN",
        "PHONE_NUMBER_ID": "PHONE_NUMBER_ID"
      },
      "command": "uvx",
      "args": [
        "whatsapp-mcp"
      ]
    }
  }
}
```