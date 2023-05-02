from project.dao import MovieDAO
from project.exceptions import ItemNotFound
from project.schemas.movie import MovieSchema
from project.services.base import BaseService


class MoviesService(BaseService):
    def get_item_by_id(self, pk):
        movie = MovieDAO(self._db_session).get_by_id(pk)
        if not movie:
            raise ItemNotFound
        return MovieSchema().dump(movie)

    def get_all_movies(self, filters, page_num, page_index=1):
        if filters.get("director_id") is not None:
            movies = MovieDAO(self._db_session).get_by_director_id(filters.get("director_id"))
        elif filters.get("genre_id") is not None:
            movies = MovieDAO(self._db_session).get_by_genre_id(filters.get("genre_id"))
        elif filters.get("year") is not None:
            movies = MovieDAO(self._db_session).get_by_year(filters.get("year"))
        elif filters.get("status") is not None:
            if filters.get("page") is not None:
                page_index = filters.get("page")
            movies = MovieDAO(self._db_session).get_by_status(page_num, page_index)
        else:
            movies = MovieDAO(self._db_session).get_all(page_num)
        return movies

    def create(self, movie_d):
        movie = MovieDAO(self._db_session).create(movie_d)
        return MovieSchema(many=True).dump(movie)


    def update(self, movie_d):
        movies = MovieDAO(self._db_session).update(movie_d)
        return MovieSchema().dump(movies)

    def delete(self, rid):
        MovieDAO(self._db_session).delete(rid)
