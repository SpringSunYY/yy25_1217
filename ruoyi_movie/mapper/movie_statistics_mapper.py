from typing import List

from sqlalchemy import select, and_, desc, func

from ruoyi_admin.ext import db
from ruoyi_movie.domain.entity import Movie
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
                func.coalesce(func.sum(MoviePo.view_count), 0).label("value"),
                MoviePo.actors.label("name")
            ).select_from(MoviePo)
            stmt = stmt.where(and_(MoviePo.actors.isnot(None), MoviePo.actors != ""))
            if request.start_time and request.end_time:
                stmt = stmt.where(and_(MoviePo.publish_date >= request.start_time,
                                       MoviePo.publish_date <= request.end_time))
            stmt = stmt.group_by(MoviePo.actors)
            if request.genres:
                stmt = stmt.where(MoviePo.genres.like(f"%{request.genres}%"))
            stmt = stmt.order_by(desc("value"))
            result = db.session.execute(stmt).mappings().all()
            # 过滤掉None值和空值
            return [StatisticsPo(value=int(item.value) if item.value is not None else 0,
                                 name=str(item.name) if item.name is not None else "")
                    for item in result if item.value is not None and item.name is not None]
        except Exception as e:
            print(f"获取演员排行数据失败:{e}")
            return []

    @classmethod
    def director_rank_statistics(cls, request) -> List[StatisticsPo]:
        """
        导演评分排行
        select avg(rating) as value, directors as name
        from tb_movie
        where pub_date >= '2019-01-01'
          and pub_date <= '2019-12-31'
        group by name
        """
        try:
            stmt = select(
                func.coalesce(func.avg(MoviePo.rating), 0.0).label("value"),
                MoviePo.directors.label("name")
            ).select_from(MoviePo)
            stmt = stmt.where(and_(MoviePo.directors.isnot(None), MoviePo.directors != ""))
            if request.genres:
                stmt = stmt.where(MoviePo.genres.like(f"%{request.genres}%"))
            if request.start_time and request.end_time:
                stmt = stmt.where(and_(MoviePo.publish_date >= request.start_time,
                                       MoviePo.publish_date <= request.end_time))
            stmt = stmt.group_by(MoviePo.directors)
            stmt = stmt.order_by(desc("value"))
            result = db.session.execute(stmt).mappings().all()
            # 过滤掉None值和空值
            return [StatisticsPo(value=float(item.value) if item.value is not None else 0.0,
                                 name=str(item.name) if item.name is not None else "")
                    for item in result if item.value is not None and item.name is not None]
        except Exception as e:
            print(f"获取导演排行数据失败:{e}")
            return []

    @classmethod
    def movie_rank_statistics(cls, request)-> List[Movie]:
        """
        电影排行
        根据播放量
        """
        try:
            # 构建查询条件
            stmt = select(MoviePo)
            stmt = stmt.where(and_(MoviePo.view_count.isnot(None), MoviePo.view_count > 0))
            if request.start_time and request.end_time:
                stmt = stmt.where(and_(MoviePo.publish_date >= request.start_time,
                                       MoviePo.publish_date <= request.end_time))
            stmt = stmt.order_by(desc(MoviePo.view_count))
            if request.genres:
                stmt = stmt.where(MoviePo.genres.like(f"%{request.genres}%"))
            if request.count_number:
                stmt = stmt.limit(request.count_number)
            result = db.session.execute(stmt).scalars().all()
            return [Movie.model_validate(item) for item in result] if result else []
        except Exception as e:
            print(f"获取电影排行数据失败:{e}")
            return []

    @classmethod
    def genres_rank_statistics(cls, request):
        """
        电影分类排行
        select avg(rating) as value, directors as name
        from tb_movie
        where pub_date >= '2019-01-01'
          and pub_date <= '2019-12-31'
        group by name
        limit 1000
        """
        try:
            # 构建查询条件
            stmt = select(
                func.coalesce(func.sum(MoviePo.view_count), 0).label("value"),
                MoviePo.genres.label("name")
            ).select_from(MoviePo)
            stmt = stmt.where(and_(MoviePo.genres.isnot(None), MoviePo.genres != ""))
            if request.start_time and request.end_time:
                stmt = stmt.where(and_(MoviePo.publish_date >= request.start_time,
                                       MoviePo.publish_date <= request.end_time))
            stmt = stmt.group_by(MoviePo.genres)
            stmt = stmt.order_by(desc("value"))
            result = db.session.execute(stmt).mappings().all()
            # 过滤掉None值和空值
            return [StatisticsPo(value=int(item.value) if item.value is not None else 0,
                                 name=str(item.name) if item.name is not None else "")
                    for item in result if item.value is not None and item.name is not None]
        except Exception as e:
            print(f"获取演员排行数据失败:{e}")
        return []

    @classmethod
    def movie_rating_rank_statistics(cls, request) -> List[Movie]:
        """
           电影排行
           根据评分
       """
        try:
            # 构建查询条件
            stmt = select(MoviePo)
            stmt = stmt.where(and_(MoviePo.rating.isnot(None), MoviePo.rating > 0))
            if request.start_time and request.end_time:
                stmt = stmt.where(and_(MoviePo.publish_date >= request.start_time,
                                       MoviePo.publish_date <= request.end_time))
            stmt = stmt.order_by(desc(MoviePo.rating))
            if request.genres:
                stmt = stmt.where(MoviePo.genres.like(f"%{request.genres}%"))
            if request.count_number:
                stmt = stmt.limit(request.count_number)
            result = db.session.execute(stmt).scalars().all()
            return [Movie.model_validate(item) for item in result] if result else []
        except Exception as e:
            print(f"获取电影评分排行数据失败:{e}")
            return []
