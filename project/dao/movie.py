import sqlalchemy.sql.expression
from sqlalchemy.orm.scoping import scoped_session

from project.dao.models import Movie


class MovieDAO:
    def __init__(self, session: scoped_session):
        self._db_session = session

    def get_by_id(self, pk):
        return self._db_session.query(Movie).filter(Movie.id == pk).one_or_none()

    def get_all(self, page_num, page_index=1):
        return self._db_session.query(Movie).offset((int(page_index)-1)*page_num).all()

    def get_by_director_id(self, pk):
        return self._db_session.query(Movie).filter(Movie.director_id == pk).all()

    def get_by_genre_id(self, pk):
        return self._db_session.query(Movie).filter(Movie.genre_id == pk).all()

    def get_by_year(self, pk):
        return self._db_session.query(Movie).filter(Movie.year == pk).all()

    def get_by_status(self, page_num=1, page_index=1):
        desc_filter = sqlalchemy.sql.expression.desc(Movie.year)
        return self._db_session.query(Movie).order_by(desc_filter).offset((int(page_index)-1)*page_num)

    def create(self, movie_d):
        ent = Movie(**movie_d)
        self._db_session.add(ent)
        self._db_session.commit()
        return ent

    def delete(self, rid):
        movie = self.get_by_id(rid)
        self._db_session.delete(movie)
        self._db_session.commit()

    def update(self, movie_d):
        movie = self.get_by_id(movie_d.get("id"))
        movie.title = movie_d.get("title")
        movie.description = movie_d.get("description")
        movie.trailer = movie_d.get("trailer")
        movie.year = movie_d.get("year")
        movie.rating = movie_d.get("rating")
        movie.genre_id = movie_d.get("genre_id")
        movie.director_id = movie_d.get("director_id")

        self._db_session.add(movie)
        self._db_session.commit()