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

from justAnotherKahootBot.fetcher.parse import Parsers

# const
api = "https://play.kahoot.it/rest/kahoots/"



class FetcherErrorType(Enum):
    NETWORK_ERROR = auto()
    PARSE_ERROR = auto()


class FetcherError(Exception):
    """
    Fetcher-related errors.

    Attributes:
        message (str): Human-readable error message.
        original_exception (Exception, optional): Original exception that caused this error.
    """

    def __init__(self, type: FetcherErrorType, reason: str, /, original_exception: Exception = None):
        super().__init__(reason)
        self.type = type
        self.original_exception = original_exception

        match type:
            case FetcherErrorType.NETWORK_ERROR:
                if not isinstance(original_exception, httpx.HTTPError):
                    raise TypeError(
                        "FetcherErrorType.NETWORK_ERROR requires original_exception to be a Httpx HTTPError"
                    )
                return f"{self.reason} (caused by {repr(original_exception)})"
            case FetcherErrorType.PARSE_ERROR:
                
                if not isinstance(original_exception, pydantic.ValidationError):
                    raise TypeError(
                        "FetcherErrorType.PARSE_ERROR requires original_exception to be a Pydantic ValidationError"
                    )
                
                if args.verbosity >= 3:
                    include_input_flag = True
                else:
                    include_input_flag = False

                self.reason = f"{reason}\nAmount of Validation Errors: {original_exception.error_count()}\n(caused by: {original_exception.errors(
                    include_context=True, 
                    include_input=include_input_flag,
                    include_url=False
                )})"
    
    def reason():
        """The Reason for the error"""
        


    def __str__(self): 
        return self.reason



class Fetcher:

    def __init__(self, raw: KahootQuiz):
        # to parse
        self.__raw = raw

        # parsed

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

    def _parse():
        pass

    @classmethod
    async def fetch_all(cls, uuid: str, retry: int = 1, retry_increment: int = 5, headers: dict = None):
        """"""
        if headers is None:
            headers = cls._get_headers()
         
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
        print(model)
        return Fetcher(model)
    
    @cache
    def __get_correct_indices(self):
        """
        Gets the correct indices for each question's choices. This is what you will be sending back to Kahoot.

        Returns:
            dict[int, int | None]: Mapping of question index to the index of the correct choice.
                If a question has no choices, the value is None.

        Example:
            >>> fetcher.get_correct_indices()
            {0: 2, 1: 0, 2: 3, 3: None}
        """
        
        d = defaultdict(dict)
        
        if self.__raw.questions is []: return d

        for index, question in enumerate(self.__raw.questions): 
            
            if question.choices is None:
                d[index] = None
            
            
            d[index] = next((i for i, c in enumerate(question.choices) if c.correct), None)

        return d
    
    @cache  
    def __get_correct_answers(self):
        """
        Gets the correct answer text for each question's choices.

        Returns:
            dict[int, str]: Mapping of question index to the text of the correct choice.
                If a question has no choices, the value is None.

        Example:
            >>> fetcher.get_correct_indices()
            {0: "Chicago, Illinois", 1: "The Sandwich King"}
        """
        
        d = defaultdict(dict)
        
        if self.__model.questions is []: return d

        for index, question in enumerate(self.__model.questions): 
            
            if question.choices is None:
                d[index] = None
            
            
            d[index] = next((c.answer for c in question.choices if c.correct), None)

        return d
    
    @cache 
    def get_question_types(self):
        """
        Gets the question type for each question in the quiz.

        Returns:
            dict[int, str | None]: Mapping of question index to its question type.
                If a question type is unavailable, the value is None.

        Example:
            >>> fetcher.__get_question_types()
            {0: "quiz", 1: "true_false", 2: "word_cloud"}
        """

        d = defaultdict(dict)

        if self.__model.questions is []: return d

        for index, question in enumerate(self.__model.questions): 
            
            d[index] = question.question_type
            print(question.question_type)

        return d

    def get_correct_indice(self, index: int):
        """
        Gets the correct choice index for a specific question.

        Args:
            index (int): The index of the question in the quiz.

        Returns:
            int | None: The index of the correct choice for the given question.
                Returns None if the question has no choices.

        Example:
            >>> fetcher.get_correct_indice(0)
            2
            # First question's correct choice is at index 2
        """
        return self.__get_correct_indices()[index]

    def get_correct_answer(self, index: int):
        """
        Gets the correct answer text for a specific question.

        Args:
            index (int): The index of the question in the quiz.

        Returns:
            str | None: The text of the correct choice for the given question.
                Returns None if the question has no choices.

        Example:
            >>> fetcher.get_correct_answer(0)
            "Beijing, China"
            # Returns the text of the first question's correct answer
        """
        return self.__get_correct_answers()[index]


    


async def main():
    f = await Fetcher.fetch_all("fd21a167-00fb-49a8-aae3-a9359c661c2c")
    print(f.get_correct_indice(7))

asyncio.run(main())
