import pytest
from justAnotherKahootBot.fetcher.fetcher import Fetcher

@pytest.mark.asyncio
async def test_fetch_and_parser():
    fetcher = Fetcher()

    quiz_uuid = "49087cb1-4352-4d03-a32a-1e3a7c44c058"

    await fetcher.fetch_all(quiz_uuid, 5)

    parser = fetcher.get_parser(0)

    # Check basic parser functionality
    assert parser is not None
    assert parser.get_question_type() == "quiz"
    assert parser.correct() == [2]
    assert parser.incorrect() == [0, 1, 3]
    assert parser.random() in [0, 1, 2, 3]
    assert parser.question_text() == "What is Jeff Bezos´s Net worth"
    assert parser.has_choices() is True
