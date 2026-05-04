import os
from typing import List

from dotenv import load_dotenv
from langchain.tools import tool

from exceptions.exceptionHandling import AppException, ExternalServiceError
from utils.place_info_search import GooglePlaceSearchTool, TavilyPlaceSearchTool


class PlaceSearchTool:
    def __init__(self):
        load_dotenv()
        self.google_api_key = os.environ.get("GPLACES_API_KEY") or os.environ.get("GPLACE_API_KEY")
        self.tavily_api_key = os.environ.get("TAVILY_API_KEY") or os.environ.get("TAVILAY_API_KEY")

        if self.google_api_key:
            os.environ.setdefault("GPLACES_API_KEY", self.google_api_key)
        if self.tavily_api_key:
            os.environ.setdefault("TAVILY_API_KEY", self.tavily_api_key)

        self.google_places_search = (
            GooglePlaceSearchTool(self.google_api_key) if self.google_api_key else None
        )
        self.tavily_search = TavilyPlaceSearchTool()
        self.place_search_tool_list = self._setup_tools()

    def _fallback_message(self, tool_name: str) -> str:
        return (
            f"{tool_name} is not configured. Add either `GPLACES_API_KEY`/`GPLACE_API_KEY` "
            "or `TAVILY_API_KEY`/`TAVILAY_API_KEY`. Until then, tell the user live place search "
            "is unavailable and give clearly labeled general suggestions only."
        )

    def _setup_tools(self) -> List:
        """Setup all tools for the place search tool"""

        @tool
        def search_attractions(place: str) -> str:
            """Search attractions of a place"""
            try:
                attraction_result = (
                    self.google_places_search.google_search_attractions(place)
                    if self.google_places_search
                    else None
                )
                if attraction_result:
                    return f"Following are the attractions of {place} as suggested by google: {attraction_result}"
            except AppException as e:
                if self.tavily_api_key:
                    try:
                        tavily_result = self.tavily_search.tavily_search_attractions(place)
                        return f"Google cannot find the details due to {e.message}. \nFollowing are the attractions of {place}: {tavily_result}"
                    except ExternalServiceError as tavily_error:
                        return tavily_error.message
                return e.message

            if self.tavily_api_key:
                try:
                    tavily_result = self.tavily_search.tavily_search_attractions(place)
                    return f"Following are the attractions of {place}: {tavily_result}"
                except AppException as exc:
                    return exc.message
            return self._fallback_message("Attraction search")

        @tool
        def search_restaurants(place: str) -> str:
            """Search restaurants of a place"""
            try:
                restaurants_result = (
                    self.google_places_search.google_search_restaurants(place)
                    if self.google_places_search
                    else None
                )
                if restaurants_result:
                    return f"Following are the restaurants of {place} as suggested by google: {restaurants_result}"
            except AppException as e:
                if self.tavily_api_key:
                    try:
                        tavily_result = self.tavily_search.tavily_search_restaurants(place)
                        return f"Google cannot find the details due to {e.message}. \nFollowing are the restaurants of {place}: {tavily_result}"
                    except ExternalServiceError as tavily_error:
                        return tavily_error.message
                return e.message

            if self.tavily_api_key:
                try:
                    tavily_result = self.tavily_search.tavily_search_restaurants(place)
                    return f"Following are the restaurants of {place}: {tavily_result}"
                except AppException as exc:
                    return exc.message
            return self._fallback_message("Restaurant search")

        @tool
        def search_activities(place: str) -> str:
            """Search activities of a place"""
            try:
                activities_result = (
                    self.google_places_search.google_search_activity(place)
                    if self.google_places_search
                    else None
                )
                if activities_result:
                    return f"Following are the activities in and around {place} as suggested by google: {activities_result}"
            except AppException as e:
                if self.tavily_api_key:
                    try:
                        tavily_result = self.tavily_search.tavily_search_activity(place)
                        return f"Google cannot find the details due to {e.message}. \nFollowing are the activities of {place}: {tavily_result}"
                    except ExternalServiceError as tavily_error:
                        return tavily_error.message
                return e.message

            if self.tavily_api_key:
                try:
                    tavily_result = self.tavily_search.tavily_search_activity(place)
                    return f"Following are the activities of {place}: {tavily_result}"
                except AppException as exc:
                    return exc.message
            return self._fallback_message("Activity search")

        @tool
        def search_transportation(place: str) -> str:
            """Search transportation of a place"""
            try:
                transportation_result = (
                    self.google_places_search.google_search_transportation(place)
                    if self.google_places_search
                    else None
                )
                if transportation_result:
                    return (
                        f"Following are the modes of transportation available in {place} "
                        f"as suggested by google: {transportation_result}"
                    )
            except AppException as e:
                if self.tavily_api_key:
                    try:
                        tavily_result = self.tavily_search.tavily_search_transportation(place)
                        return f"Google cannot find the details due to {e.message}. \nFollowing are the modes of transportation available in {place}: {tavily_result}"
                    except ExternalServiceError as tavily_error:
                        return tavily_error.message
                return e.message

            if self.tavily_api_key:
                try:
                    tavily_result = self.tavily_search.tavily_search_transportation(place)
                    return f"Following are the modes of transportation available in {place}: {tavily_result}"
                except AppException as exc:
                    return exc.message
            return self._fallback_message("Transportation search")

        return [search_attractions, search_restaurants, search_activities, search_transportation]
