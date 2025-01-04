import os
import logging
import sys
from datetime import datetime
from tavily import TavilyClient
from dotenv import load_dotenv
from fastmcp import FastMCP

# 设置默认编码为UTF-8
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass  # Python 3.7以下版本不支持reconfigure

# 读取环境变量
load_dotenv()
# 准备日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("mcp2tavily")
# Create an MCP server
mcp = FastMCP("mcp2tavily", dependencies=["tavily-python", "python-dotenv"])
# 准备API密钥
API_KEY = os.getenv("TAVILY_API_KEY")
if not API_KEY:
    logger.error("TAVILY_API_KEY environment variable not found")
    raise ValueError("TAVILY_API_KEY environment variable required")

def _do_search(query: str) -> str:
    """Internal function to handle the search logic with UTF-8 support"""
    try:
        # 确保查询字符串是UTF-8编码
        query = query.encode('utf-8').decode('utf-8')
        tavily_client = TavilyClient(api_key=API_KEY)
        response = tavily_client.search(
            query=query,
            search_depth="basic",
            include_answer=True,
            include_raw_content=False
        )
        
        # 确保响应文本是UTF-8编码
        answer = response.get('answer', 'No answer found').encode('utf-8').decode('utf-8')
        sources = response.get('sources', [])
        
        result = f"Answer: {answer}\n\nSources:"
        for source in sources[:3]:
            title = source.get('title', 'No title').encode('utf-8').decode('utf-8')
            url = source.get('url', 'No URL')
            result += f"\n- {title}: {url}"
            
        return result
    except UnicodeError as e:
        logger.error(f"Encoding error: {str(e)}")
        return "Error: Unicode encoding issue occurred"
    except Exception as e:
        logger.error(f"Search error: {str(e)}")
        return f"Error performing search: {str(e)}"

@mcp.tool()
def search_web(query: str) -> str:
    """Search the web for information using Tavily API"""
    return _do_search(query)

@mcp.tool()
def search_web_info(query: str) -> str:
    """从网络搜索用户查询的信息"""
    return _do_search(query)