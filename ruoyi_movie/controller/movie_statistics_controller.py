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
    return AjaxResponse.from_success(data=movie_statistics_service.actor_rank_statistics(request))
