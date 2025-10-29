import pytest
from justAnotherKahootBot.fetcher.fetcher import Fetcher

@pytest.mark.asyncio
async def test_fetch_and_parser():
    fetcher = Fetcher()

    quiz_uuid = "8728fd0b-8c3f-4f78-9807-969beaee6ec1"

    await fetcher.fetch_all(quiz_uuid)

    parser = fetcher.get_parser(0)

    # Check basic parser functionality
    assert parser is not None
    assert parser.get_question_type() is "Quiz"
    assert parser.correct() is [1]
    assert parser.incorrect() [0, 2, 3]
    assert parser.random() in [0, 1, 2, 3]
    assert parser.question_text() is "Quiz"
    assert parser.has_choices() is True
