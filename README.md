# MCP2Tavily

A MCP protocol server that implements web search functionality using the Tavily API.

## Prerequisites

- Python 3.8+
- UV package manager
- Tavily API key

## Installation

1. Clone the repository
```bash
git clone <repository-url>
cd mcp2tavily
```

2. Create and edit the `.env` file
```bash
# Create .env file
touch .env
# Add your Tavily API key to .env
echo "TAVILY_API_KEY=your_api_key_here" > .env
```

3. Set up virtual environment with UV
```bash
# Create and activate virtual environment
uv venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
```

4. Install dependencies
```bash
uv sync
```

## Usage

### Install as Claude extension
```bash
fastmcp install mcp2tavily.py
```

### Development mode with MCP Inspector
To test the functionality using MCP Inspector:

```bash
fastmcp dev mcp2tavily.py
```

Once running, you can access the MCP Inspector at: http://localhost:5173

## Available Tools

- `search_web(query: str)`: Search the web using Tavily API
- `search_web_info(query: str)`: Same as above, with Chinese description

## Environment Variables

- `TAVILY_API_KEY`: Your Tavily API key (required)

## 手动添加Cline Continue Claude
打开Cline Continue Claude的MCP服务器配置文件，加入以下信息
"mcp2tavily": {
      "command": "uv",
      "args": [
        "run",
        "--with",
        "fastmcp",
        "--with",
        "python-dotenv",
        "--with",
        "tavily-python",
        "fastmcp",
        "run",
        "C:\\Users\\你的真实路径\\mcp2tavily.py"
      ],
      "env": {
        "TAVILY_API_KEY": "API密钥"
      }
    }
