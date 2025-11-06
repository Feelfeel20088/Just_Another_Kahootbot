from enum import Enum, auto
from typing import Any, Dict, List, Type, Optional
from .kahoot_model import Question
import random
from typing import Protocol

class QuizTypes(Enum):
    scale = "scale"
    content = "content"
    word_cloud = "word_cloud"
    survey = "survey"
    brainstorming = "brainstorming"
    drop_pin = "drop_pin"
    multiple_select_poll = "multiple_select_poll"
    jumble = "jumble"
    nps = "nps"
    feedback = "feedback"
    pin_it = "pin_it"
    quiz = "quiz"
    true_or_false = "true_or_false" # need to get actual value



class QuestionParserProtocol(Protocol):
    def correct_index(self) -> List[int]:
        """Return the index of the correct choice"""
        ...

    def incorrect_index(self) -> List[int]:
        """Return an index of an incorrect choice"""
        ...

    def correct(self) -> Optional[int | str]:
        """Return an value of an incorrect choice"""
        ...

    def incorrect(self) -> Optional[int | str]:
        """Return the value of the correct choice"""
        ...

    def random_index(self) -> Optional[int]:
        """Return a random choice index"""
        ...

    def question_text(self) -> str:
        """Return the text of the question"""
        ...

    def has_choices(self) -> bool:
        """Whether the question has choices"""
        ...




class BaseQuestionParser:
    
    def __init__(self, q: Question):
        self._question = q
    
    def get_question_type(self) -> Optional[str]:
        return self._question.question_type
    
    def get_time(self) -> Optional[int]:
        return self._question.time

    def get_points(self) -> Optional[bool]:
        return self._question.points 

    def get_points_multiplier(self) -> Optional[int]:
        return self._question.pointsMultiplier

    def get_resources(self) -> Optional[str]:
        return self._question.resources

    def get_question_format(self) -> Optional[int]:
        return self._question.questionFormat

    def get_media(self) -> Optional[List]:
        return self._question.media
        
# This parser handles standard quiz questions, including True/False style questions.
class QuizParser(BaseQuestionParser, QuestionParserProtocol):
    def __init__(self, q: Question):
        super().__init__(q)

    def correct_index(self) -> List[int]:
        return [i for i, c in enumerate(self._question.choices) if c.correct]

    def incorrect_index(self) -> List[int]:
        return [i for i, c in enumerate(self._question.choices) if not c.correct]
    
    def correct(self):
        return self.correct_index()
    
    def incorrect(self):
        return self.incorrect_index()

    def random_index(self) -> Optional[int]:
        return random.randrange(len(self._question.choices))

    def question_text(self) -> str:
        return self._question.question

    def has_choices(self) -> bool:
        return True

class ScaleParser(BaseQuestionParser):
    def parse(self, data: Question) -> dict:
        pass

class WordCloudParser(BaseQuestionParser):
    def parse(self, data: Question) -> dict:
        pass

class OpenEndedParser(BaseQuestionParser, QuestionParserProtocol):
    def __init__(self, q: Question):
        super().__init__(q)

    def correct_index(self) -> List[int]:
        return [0]

    def incorrect_index(self) -> List[int]:
        return None
    
    def correct(self) -> Optional[int | str]:
        return self._question.choices[0].answer

    def incorrect(self) -> List[int]:
        return None

    def random_index(self) -> Optional[int]:
        return random.randrange(len(self._question.choices))

    def question_text(self) -> str:
        return self._question.question

    def has_choices(self) -> bool:
        return True


class ContentParser(BaseQuestionParser):
    def parse(self, data: Question) -> Any:
        pass


class SurveyParser(BaseQuestionParser):
    def parse(self, data: Question) -> Any:
        pass


class BrainstormingParser(BaseQuestionParser):
    def parse(self, data: Question) -> Any:
        pass


class DropPinParser(BaseQuestionParser):
    def parse(self, data: Question) -> Any:
        pass


class MultipleSelectPollParser(BaseQuestionParser):
    def parse(self, data: Question) -> Any:
        pass

# Impossible to find in response payload. Server randomly generates.
class JumbleParser(BaseQuestionParser):
    def parse(self, data: Question) -> Any:
        pass


class NPSParser(BaseQuestionParser):
    def parse(self, data: Question) -> Any:
        pass


class FeedbackParser(BaseQuestionParser):
    def parse(self, data: Question) -> Any:
        pass


class PinItParser(BaseQuestionParser):
    def parse(self, data: Question) -> Any:
        pass



class QParsers:
    """Main registry for all quiz type parsers."""

    PARSER_MAP: Dict[QuizTypes, Type[BaseQuestionParser]] = {
        QuizTypes.quiz: QuizParser,
        QuizTypes.scale: ScaleParser,
        QuizTypes.word_cloud: WordCloudParser,
        QuizTypes.content: ContentParser,
        QuizTypes.survey: SurveyParser,
        QuizTypes.brainstorming: BrainstormingParser,
        QuizTypes.drop_pin: DropPinParser,
        QuizTypes.multiple_select_poll: MultipleSelectPollParser,
        QuizTypes.jumble: JumbleParser,
        QuizTypes.nps: NPSParser,
        QuizTypes.feedback: FeedbackParser,
        QuizTypes.pin_it: PinItParser,
    }


    @classmethod
    def parse(cls, qtype: QuizTypes | str, q: Question):
        if isinstance(qtype, str):
            try:
                qtype = QuizTypes(qtype)
            except ValueError:
                raise ValueError(f"Unknown quiz type: {qtype}")

        
        parser_cls = cls.PARSER_MAP.get(qtype)
        if not parser_cls:
            raise NotImplementedError(f"No parser registered for {qtype.value}")
        
        return parser_cls(q)