import pytest

from project.dao import DirectorDAO
from project.dao.models import Director


class TestDirectorDAO:
    @pytest.fixture(autouse=True)
    def dao(self, db):
        self.dao = DirectorDAO(db.session)

    @pytest.fixture
    def director_1(self, db):
        g = Director(name="Коля")
        db.session.add(g)
        db.session.commit()
        return g

    @pytest.fixture
    def director_2(self, db):
        g = Director(name="Петя")
        db.session.add(g)
        db.session.commit()
        return g

    def test_get_director_by_id(self, director_1):
        assert self.dao.get_by_id(director_1.id) == director_1

    def test_get_director_by_id_not_found(self):
        assert self.dao.get_by_id(1) is None

    def test_get_all_directors(self, director_1, director_2):
        assert self.dao.get_all() == [director_1, director_2]
