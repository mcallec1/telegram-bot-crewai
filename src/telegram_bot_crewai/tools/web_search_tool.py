from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import os
from serpapi.google_search import GoogleSearch
import logging

logger = logging.getLogger(__name__)

class WebSearchInput(BaseModel):
    """Input for web search tool."""
    query: str = Field(..., description="The search query")

class WebSearchTool(BaseTool):
    name: str = "Web Search"
    description: str = "Search the web for the given query and returns the top result"
    args_schema: Type[BaseModel] = WebSearchInput

    def _run(self, query: str) -> str:
        logger.info(f"Executing web search for: {query}")
        try:
            params = {
                "engine": "google",
                "q": query,
                "api_key": os.getenv("SERPAPI_KEY")
            }
            logger.debug(f"Search params: {params}")
            search = GoogleSearch(params)
            results = search.get_dict()
            logger.debug(f"Search results: {results}")
            
            if "error" in results:
                logger.error(f"Search API error: {results['error']}")
                return f"Search error: {results['error']}"
            
            organic_results = results.get("organic_results", [])
            if not organic_results:
                logger.warning("No search results found")
                return "No results found."
                
            first_result = organic_results[0]
            logger.info("Successfully retrieved search result")
            return f"{first_result.get('title', 'No title')}\n{first_result.get('snippet', 'No description')}\n{first_result.get('link', 'No link')}"
        except Exception as e:
            logger.error(f"Web search error: {e}", exc_info=True)
            return f"Web search error: {e}"

web_search_tool = WebSearchTool() 