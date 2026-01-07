from typing import List

from ruoyi_framework.descriptor import custom_cacheable
from ruoyi_movie.domain.entity import Movie
from ruoyi_movie.domain.statistics.vo import StatisticsVo
from ruoyi_movie.domain.statistics.vo.statistics_vo import PieBarStatisticsVo
from ruoyi_movie.mapper.movie_statistics_mapper import MovieStatisticsMapper


class MovieStatisticsService:
    """电影统计分析"""

    @classmethod
    @custom_cacheable(
        key_prefix="movie:statistics:actor:rank",
        use_query_params_as_key=True,
        expire_time=5 * 60
    )
    def actor_rank_statistics(cls, request) -> List[StatisticsVo]:
        """演员票房排行"""
        pos = MovieStatisticsMapper.actor_rank_statistics(request)
        # 构建返回结果，演员以/分割，所以需要清洗数据
        if pos is None:
            return []
        result = {}
        for po in pos:
            if po.name is None:
                continue
            actors = po.name.split('/')
            for actor in actors:
                if actor not in result:
                    result[actor] = po.value
                else:
                    result[actor] += po.value
        # 根据value排序
        result = sorted(result.items(), key=lambda x: x[1], reverse=True)
        # 返回n条
        result = result[:request.count_number]
        return [StatisticsVo(name=name, value=value, tooltipText="", moreInfo="") for name, value in result]

    @classmethod
    @custom_cacheable(
        key_prefix="movie:statistics:director:rank",
        use_query_params_as_key=True,
        expire_time=5 * 60
    )
    def director_rank_statistics(cls, request) -> List[StatisticsVo]:
        """导演评分排行"""
        pos = MovieStatisticsMapper.director_rank_statistics(request)
        # 构建返回结果，导演以/分割，所以需要清洗数据
        if pos is None:
            return []
        result = {}
        for po in pos:
            if po.name is None:
                continue
            directors = po.name.split('/')
            for director in directors:
                if director not in result:
                    result[director] = po.value
                else:
                    # 标识已经有了，要重新计算平均分
                    result[director] = (result[director] + po.value) / 2
        # 根据value排序,并且保留两位小数
        result = sorted(result.items(), key=lambda x: x[1], reverse=True)
        result = result[:request.count_number]
        return [StatisticsVo(name=name, value=round(value, 2), tooltipText="", moreInfo="") for name, value in
                result]

    @classmethod
    @custom_cacheable(
        key_prefix="movie:statistics:movie:rank",
        use_query_params_as_key=True,
        expire_time=5 * 60
    )
    def movie_rank_statistics(cls, request) -> List[Movie]:
        """电影排行"""
        return MovieStatisticsMapper.movie_rank_statistics(request)

    @classmethod
    @custom_cacheable(
        key_prefix="movie:statistics:genres:rank",
        use_query_params_as_key=True,
        expire_time=5 * 60
    )
    def genres_rank_statistics(cls, request) -> List[PieBarStatisticsVo]:
        """电影类型排行"""
        pos = MovieStatisticsMapper.genres_rank_statistics(request)
        if pos is None:
            return []
        result = {}
        for po in pos:
            if po.name is None:
                continue
            genres = po.name.split('/')
            for genre in genres:
                if genre not in result:
                    result[genre] = po.value
                else:
                    result[genre] += po.value
        # 只要前十，按票房总和降序排序后取前10个
        result = dict(sorted(result.items(), key=lambda x: x[1], reverse=True)[:10])
        # 遍历结果，拿到每个类型里面的电影排行
        result_list = []
        for key, total_value in result.items():
            request.genres = key
            movies = MovieStatisticsMapper.movie_rating_rank_statistics(request)
            values = []
            for movie in movies:
                values.append(
                    StatisticsVo(name=movie.title, value=round(movie.rating, 2) if movie.rating else 0.0,
                                        tooltipText="", moreInfo="", movieId=movie.movie_id))
            result_list.append(PieBarStatisticsVo(name=key, tooltipText="", value=total_value, values=values))
        return result_list
