import pytest
from sqlalchemy.orm import Session

from tests.factories.items import ItemFactory


@pytest.fixture
def item_factory(session: Session) -> ItemFactory:
    return ItemFactory(session=session)
