from ruoyi_common.base.model import AjaxResponse
from ruoyi_common.descriptor.serializer import JsonSerializer
from ruoyi_common.descriptor.validator import QueryValidator
from ruoyi_framework.descriptor.permission import HasPerm, PreAuthorize
from ruoyi_movie.controller import movie_statistics as movie_statistics_bp
from ruoyi_movie.domain.statistics.dto import MovieStatisticsRequest
from ruoyi_movie.service.movie_statistics_service import MovieStatisticsService

gen = movie_statistics_bp
movie_statistics_service = MovieStatisticsService()


@gen.route('/actor/rank', methods=['GET'])
@QueryValidator(is_page=False)
@PreAuthorize(HasPerm('movie:statistics:list'))
@JsonSerializer()
def actor_rank_statistics(request: MovieStatisticsRequest):
    """演员票房排行"""
    print(request)
    request_entity=MovieStatisticsRequest()
    for attr in request.model_fields.keys():
        if hasattr(request_entity, attr):
            setattr(request_entity, attr, getattr(request, attr))
    return AjaxResponse.from_success(data=movie_statistics_service.actor_rank_statistics(request_entity))

#导演评分排行
@gen.route('/director/rank', methods=['GET'])
@QueryValidator(is_page=False)
@PreAuthorize(HasPerm('movie:statistics:list'))
@JsonSerializer()
def director_rank_statistics(request: MovieStatisticsRequest):
    """导演评分排行"""
    request_entity=MovieStatisticsRequest()
    for attr in request.model_fields.keys():
        if hasattr(request_entity, attr):
            setattr(request_entity, attr, getattr(request, attr))
    return AjaxResponse.from_success(data=movie_statistics_service.director_rank_statistics(request_entity))


#电影排行
@gen.route('/movie/rank', methods=['GET'])
@QueryValidator(is_page=False)
@PreAuthorize(HasPerm('movie:statistics:list'))
@JsonSerializer()
def movie_rank_statistics(request: MovieStatisticsRequest):
    """电影排行"""
    request_entity=MovieStatisticsRequest()
    for attr in request.model_fields.keys():
        if hasattr(request_entity, attr):
            setattr(request_entity, attr, getattr(request, attr))
    return AjaxResponse.from_success(data=movie_statistics_service.movie_rank_statistics(request_entity))

#电影类型排行
@gen.route('/genres/rank', methods=['GET'])
@QueryValidator(is_page=False)
@PreAuthorize(HasPerm('movie:statistics:list'))
@JsonSerializer()
def genres_rank_statistics(request: MovieStatisticsRequest):
    """电影类型排行"""
    request_entity=MovieStatisticsRequest()
    for attr in request.model_fields.keys():
        if hasattr(request_entity, attr):
            setattr(request_entity, attr, getattr(request, attr))
    return AjaxResponse.from_success(data=movie_statistics_service.genres_rank_statistics(request_entity))
