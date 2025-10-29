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



class QuestionParserProtocol(Protocol):
    def correct(self) -> List[int]:
        """Return the index of the correct choice"""
        ...

    def incorrect(self) -> List[int]:
        """Return an index of an incorrect choice"""
        ...

    def random(self) -> int:
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
        return self._question.question_type if self._question and self._question.question_type is not None else None

    def get_time(self) -> Optional[int]:
        return self._question.time if self._question and self._question.time is not None else None

    def get_points(self) -> Optional[bool]:
        return self._question.points if self._question and self._question.points is not None else None

    def get_points_multiplier(self) -> Optional[int]:
        return self._question.pointsMultiplier if self._question and self._question.pointsMultiplier is not None else None

    def get_resources(self) -> Optional[str]:
        return self._question.resources if self._question and self._question.resources is not None else None

    def get_question_format(self) -> Optional[int]:
        return self._question.questionFormat if self._question and self._question.questionFormat is not None else None

    def get_media(self) -> Optional[List]:
        return self._question.media if self._question and self._question.media is not None else None
        

class QuizParser(BaseQuestionParser, QuestionParserProtocol):
    def __init__(self, q: Question):
        super().__init__(q)

    def correct(self) -> List[int]:
        return [i for i, c in enumerate(self._question.choices) if c.correct]

    def incorrect(self) -> List[int]:
        return [i for i, c in enumerate(self._question.choices) if not c.correct]

    def random(self) -> int:
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