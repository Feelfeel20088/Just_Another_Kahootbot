from enum import Enum, auto
from typing import Any, Dict, Type


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



from typing import Any


class BaseParser:
    def parse(self, data: dict) -> Any:
        """All concrete parsers must implement this."""
        raise NotImplementedError(f"{self.__class__.__name__} has not implemented parse().")


class QuizParser(BaseParser):
    def parse(self, data: dict) -> dict:
        pass

class ScaleParser(BaseParser):
    def parse(self, data: dict) -> dict:
        pass

class WordCloudParser(BaseParser):
    def parse(self, data: dict) -> dict:
        pass

class ContentParser(BaseParser):
    def parse(self, data: dict) -> Any:
        pass


class SurveyParser(BaseParser):
    def parse(self, data: dict) -> Any:
        pass


class BrainstormingParser(BaseParser):
    def parse(self, data: dict) -> Any:
        pass


class DropPinParser(BaseParser):
    def parse(self, data: dict) -> Any:
        pass


class MultipleSelectPollParser(BaseParser):
    def parse(self, data: dict) -> Any:
        pass


class JumbleParser(BaseParser):
    def parse(self, data: dict) -> Any:
        pass


class NPSParser(BaseParser):
    def parse(self, data: dict) -> Any:
        pass


class FeedbackParser(BaseParser):
    def parse(self, data: dict) -> Any:
        pass


class PinItParser(BaseParser):
    def parse(self, data: dict) -> Any:
        pass



class Parsers:
    """Main registry for all quiz type parsers."""

    PARSER_MAP: Dict[QuizTypes, Type[BaseParser]] = {
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
    def parse(cls, qtype: QuizTypes | str, data: dict):
        if isinstance(qtype, str):
            try:
                qtype = QuizTypes(qtype)
            except ValueError:
                raise ValueError(f"Unknown quiz type: {qtype}")

        
        parser_cls = cls.PARSER_MAP.get(qtype)
        if not parser_cls:
            raise NotImplementedError(f"No parser registered for {qtype.value}")
        
        return parser_cls().parse(data)