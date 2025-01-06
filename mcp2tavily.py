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
def _get_url_content(url: str) -> str:
    """Internal function to get content from a specific URL using Tavily API"""
    try:
        tavily_client = TavilyClient(api_key=API_KEY)
        logger.info(f"Attempting to extract content from URL: {url}")
        
        response = tavily_client.extract(url)
        # logger.info(f"Raw API response: {response}")  # 使用 logger 替代 print
        
        # 处理返回的数据结构
        results = response.get('results', [])
        if not results:
            logger.error(f"No results found in response: {response}")
            return "No content found for this URL. API response contains no results."
            
        # 获取第一个结果的原始内容
        first_result = results[0]
        # logger.info(f"First result structure: {list(first_result.keys())}")  # 只记录键名，避免日志过大
        
        content = first_result.get('raw_content', '')
        if not content:
            logger.error("No raw_content found in first result")
            return "No raw content available in the API response"
        
        # 确保响应文本是UTF-8编码
        content = content.encode('utf-8').decode('utf-8')
        
        # 添加一些元数据到输出中
        metadata = f"URL: {url}\n"
        metadata += f"Content length: {len(content)} characters\n"
        metadata += "---\n\n"
        
        logger.info(f"Successfully extracted content with length: {len(content)}")
        return f"{metadata}{content}"
        
    except Exception as e:
        logger.exception(f"Detailed error while extracting URL content")
        return f"Error getting content from URL: {str(e)}"

@mcp.tool()
def search_web(query: str) -> str:
    """Search the web for information using Tavily API"""
    return _do_search(query)

@mcp.tool()
def search_web_info(query: str) -> str:
    """从网络搜索用户查询的信息"""
    return _do_search(query)

@mcp.tool()
def get_url_content(url: str) -> str:
    """Get the content from a specific URL using Tavily API
    
    Args:
        url (str): The URL to extract content from
        
    Returns:
        str: The extracted content from the URL
    """
    return _get_url_content(url)

@mcp.tool()
def get_url_content_info(url: str) -> str:
    """从指定URL获取网页内容
    
    参数:
        url (str): 需要提取内容的网页地址
        
    返回:
        str: 从URL提取的网页内容
    """
    return _get_url_content(url)