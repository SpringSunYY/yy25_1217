from typing import List
from ruoyi_movie.domain.statistics.vo import StatisticsVo
from ruoyi_movie.mapper.movie_statistics_mapper import MovieStatisticsMapper


class MovieStatisticsService:
    """电影统计分析"""

    @classmethod
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
        return [StatisticsVo(name=name, value=value) for name, value in result]

    @classmethod
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
        return [StatisticsVo(name=name, value=round(value, 2)) for name, value in result]
