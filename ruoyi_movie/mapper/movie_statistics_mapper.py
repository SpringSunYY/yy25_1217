from typing import List
from sqlalchemy import select, delete, and_, or_, desc, asc, func
from ruoyi_admin.ext import db

from ruoyi_movie.domain.po import MoviePo
from ruoyi_movie.domain.statistics.po import StatisticsPo


class MovieStatisticsMapper:
    @classmethod
    def actor_rank_statistics(cls, request) -> List[StatisticsPo]:
        """
        演员票房排行
        select sum(view_count) as value, actors as name
            from tb_movie
            where pub_date >= '2019-01-01'
              and pub_date <= '2019-12-31'
            group by actors
        """
        try:
            # 构建查询条件
            stmt = select(
                func.sum(MoviePo.view_count).label("value"),
                MoviePo.actors.label("name")
            ).select_from(MoviePo)
            if request.start_time and request.end_time:
                stmt = stmt.where(and_(MoviePo.publish_date >= request.start_time,
                                       MoviePo.pub_date <= request.end_time))
            stmt = stmt.group_by(MoviePo.actors)
            result = db.session.execute(stmt).mappings().all()
            return [StatisticsPo(value=item.value, name=str(item.name)) for item in result]
        except Exception as e:
            print(f"获取演员排行数据失败:{e}")
            return []
