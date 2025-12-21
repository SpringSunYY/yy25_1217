# -*- coding: utf-8 -*-
# @Module: ruoyi_movie/controller

from flask import Blueprint

view = Blueprint('view', __name__, url_prefix='/movie/view')
recommend = Blueprint('recommend', __name__, url_prefix='/movie/recommend')
movie_review = Blueprint('movie_review', __name__, url_prefix='/movie/movieReview')
movie = Blueprint('movie', __name__, url_prefix='/movie/movie')
like = Blueprint('like', __name__, url_prefix='/movie/like')


from . import view_controller
from . import recommend_controller
from . import movie_review_controller
from . import movie_controller
from . import like_controller
