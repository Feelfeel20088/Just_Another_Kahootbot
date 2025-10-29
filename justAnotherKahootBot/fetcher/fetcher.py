import asyncio
from collections import defaultdict
from functools import cache
import httpx
import time
import random
import orjson
import pydantic
from enum import Enum, auto
from justAnotherKahootBot.fetcher.kahoot_model import KahootQuiz

from justAnotherKahootBot.fetcher.parse import QParsers

from justAnotherKahootBot.config.state import args

# const
api = "https://play.kahoot.it/rest/kahoots/"



class FetcherErrorType(Enum):
    NETWORK_ERROR = auto()
    PARSE_ERROR = auto()


class FetcherError(Exception):
    def __init__(self, type: FetcherErrorType, reason: str, /, original_exception: Exception = None):
        self.type = type
        self.original_exception = original_exception

        match type:
            case FetcherErrorType.NETWORK_ERROR:
                if not isinstance(original_exception, httpx.HTTPError):
                    raise TypeError(
                        "FetcherErrorType.NETWORK_ERROR requires original_exception to be a Httpx HTTPError"
                    )
                self.reason = f"{reason} (caused by {repr(original_exception)})"

            case FetcherErrorType.PARSE_ERROR:
                if not isinstance(original_exception, pydantic.ValidationError):
                    raise TypeError(
                        "FetcherErrorType.PARSE_ERROR requires original_exception to be a Pydantic ValidationError"
                    )
                include_input_flag = args.verbosity >= 3
                self.reason = (
                    f"{reason}\n"
                    f"Amount of Validation Errors: {original_exception.error_count()}\n"
                    f"(caused by: {original_exception.errors(include_context=True, include_input=include_input_flag, include_url=False)})"
                )

        super().__init__(self.reason)

    def __str__(self):
        return self.reason




class Fetcher:

    def __init__(self):
        # to parse
        
        self.__raw = None

    @classmethod
    def _get_headers(cls):
        return {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0",
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache'
        }

    async def fetch_all(self, uuid: str, retry: int = 1, retry_increment: int = 5, headers: dict = None):
        """"""
        if headers is None:
            headers = Fetcher._get_headers()
         
        async with httpx.AsyncClient() as client:
            for r in range(retry):
                try:
                    response = await client.get(f"{api}{uuid}", headers=headers)

                    response.raise_for_status()

                    break

                except httpx.HTTPError as e:
                    if r == retry - 1:
                        raise FetcherError(
                            FetcherErrorType.NETWORK_ERROR,
                            "Could not connect to Kahoot REST API",
                            e
                        )
                    
                await asyncio.sleep(retry_increment)    

        json = orjson.loads(response.text)
        try: 
            model = KahootQuiz.model_validate(
                json, 
                strict=True, 
                from_attributes=True,
                
            )

        except pydantic.ValidationError as e:
            
            raise FetcherError(
                FetcherErrorType.PARSE_ERROR,
                "Invalid data presented to the pydantic parser.",
                e
            )
        
        self.__raw = model
    
    def get_parser(self, question_index: int):
        return QParsers.parse(self.__raw.questions[question_index].question_type, self.__raw.questions[question_index])