# -*- coding: utf-8 -*-
# @Author  : YY
# @FileName: recommend_mapper.py
# @Time    : 2026-01-02 18:33:22

from typing import List, Optional
from datetime import datetime

from flask import g
from sqlalchemy import select, update, delete

from ruoyi_admin.ext import db
from ruoyi_movie.domain.entity import Recommend
from ruoyi_movie.domain.po import RecommendPo
from ruoyi_movie.mapper.view_mapper import ViewMapper
from ruoyi_movie.mapper.like_mapper import LikeMapper
from ruoyi_movie.mapper.movie_mapper import MovieMapper

class RecommendMapper:
    """用户推荐Mapper"""

    @classmethod
    def select_recommend_list(cls, recommend: Recommend) -> List[Recommend]:
        """
        查询用户推荐列表

        Args:
            recommend (recommend): 用户推荐对象

        Returns:
            List[recommend]: 用户推荐列表
        """
        try:
            # 构建查询条件
            stmt = select(RecommendPo)

            if recommend.id is not None:
                stmt = stmt.where(RecommendPo.id == recommend.id)

            if recommend.user_id is not None:
                stmt = stmt.where(RecommendPo.user_id == recommend.user_id)

            if recommend.user_name:
                stmt = stmt.where(RecommendPo.user_name.like("%" + str(recommend.user_name) + "%"))

            _params = getattr(recommend, "params", {}) or {}
            begin_val = _params.get("beginCreateTime")
            end_val = _params.get("endCreateTime")
            if begin_val is not None:
                stmt = stmt.where(RecommendPo.create_time >= begin_val)
            if end_val is not None:
                stmt = stmt.where(RecommendPo.create_time <= end_val)

            if "criterian_meta" in g and g.criterian_meta.page:
                g.criterian_meta.page.stmt = stmt
            #创建时间倒叙
            stmt = stmt.order_by(RecommendPo.create_time.desc())
            result = db.session.execute(stmt).scalars().all()
            return [Recommend.model_validate(item) for item in result] if result else []
        except Exception as e:
            print(f"查询用户推荐列表出错: {e}")
            return []


    @classmethod
    def select_recommend_by_id(cls, id: int) -> Optional[Recommend]:
        """
        根据ID查询用户推荐

        Args:
            id (int): 推荐编号

        Returns:
            recommend: 用户推荐对象
        """
        try:
            result = db.session.get(RecommendPo, id)
            return Recommend.model_validate(result) if result else None
        except Exception as e:
            print(f"根据ID查询用户推荐出错: {e}")
            return None


    @classmethod
    def insert_recommend(cls, recommend: Recommend) -> int:
        """
        新增用户推荐

        Args:
            recommend (recommend): 用户推荐对象

        Returns:
            int: 插入的记录数
        """
        try:
            now = datetime.now()
            new_po = RecommendPo()
            new_po.id = recommend.id
            new_po.user_id = recommend.user_id
            new_po.user_name = recommend.user_name
            new_po.content = recommend.content
            new_po.model_info = recommend.model_info
            new_po.create_time = recommend.create_time or now
            db.session.add(new_po)
            db.session.commit()
            recommend.id = new_po.id
            return 1
        except Exception as e:
            db.session.rollback()
            print(f"新增用户推荐出错: {e}")
            return 0


    @classmethod
    def update_recommend(cls, recommend: Recommend) -> int:
        """
        修改用户推荐

        Args:
            recommend (recommend): 用户推荐对象

        Returns:
            int: 更新的记录数
        """
        try:

            existing = db.session.get(RecommendPo, recommend.id)
            if not existing:
                return 0
            now = datetime.now()
            # 主键不参与更新
            existing.user_id = recommend.user_id
            existing.user_name = recommend.user_name
            existing.content = recommend.content
            existing.model_info = recommend.model_info
            existing.create_time = recommend.create_time
            db.session.commit()
            return 1

        except Exception as e:
            db.session.rollback()
            print(f"修改用户推荐出错: {e}")
            return 0

    @classmethod
    def delete_recommend_by_ids(cls, ids: List[int]) -> int:
        """
        批量删除用户推荐

        Args:
            ids (List[int]): ID列表

        Returns:
            int: 删除的记录数
        """
        try:
            stmt = delete(RecommendPo).where(RecommendPo.id.in_(ids))
            result = db.session.execute(stmt)
            db.session.commit()
            return result.rowcount
        except Exception as e:
            db.session.rollback()
            print(f"批量删除用户推荐出错: {e}")
            return 0

    @classmethod
    def select_user_views_by_user_id(cls, user_id: int, days: int = 30):
        """
        根据用户ID获取最近N天的浏览记录

        Args:
            user_id (int): 用户ID
            days (int): 最近天数，默认30天

        Returns:
            List[View]: 用户浏览记录列表
        """
        # 直接调用ViewMapper的方法
        return ViewMapper.select_user_views_by_user_id(user_id, days)

    @classmethod
    def select_user_likes_by_user_id(cls, user_id: int, days: int = 30):
        """
        根据用户ID获取最近N天的点赞记录

        Args:
            user_id (int): 用户ID
            days (int): 最近天数，默认30天

        Returns:
            List[Like]: 用户点赞记录列表
        """
        # 直接调用LikeMapper的方法
        return LikeMapper.select_user_likes_by_user_id(user_id, days)

    @classmethod
    def select_user_views_after_time(cls, user_id: int, after_time):
        """
        根据用户ID获取某个时间点之后的所有浏览记录

        Args:
            user_id (int): 用户ID
            after_time (datetime): 时间点

        Returns:
            List[View]: 用户浏览记录列表
        """
        # 直接调用ViewMapper的方法
        return ViewMapper.select_user_views_after_time(user_id, after_time)

    @classmethod
    def select_user_likes_after_time(cls, user_id: int, after_time):
        """
        根据用户ID获取某个时间点之后的所有点赞记录

        Args:
            user_id (int): 用户ID
            after_time (datetime): 时间点

        Returns:
            List[Like]: 用户点赞记录列表
        """
        # 直接调用LikeMapper的方法
        return LikeMapper.select_user_likes_after_time(user_id, after_time)

    @classmethod
    def select_similar_movies(cls, genres: str = None, directors: str = None,
                             country: str = None, actors: str = None,
                             exclude_movie_ids: List[int] = None,
                             limit: int = 20):
        """
        根据维度信息查找相似的电影

        Args:
            genres (str): 类型
            directors (str): 导演
            country (str): 国家地区
            actors (str): 主演
            exclude_movie_ids (List[int]): 排除的电影ID列表
            limit (int): 返回数量限制

        Returns:
            List[Movie]: 相似电影列表
        """
        # 直接调用MovieMapper的方法
        return MovieMapper.select_similar_movies_by_dimensions(
            genres=genres,
            directors=directors,
            country=country,
            actors=actors,
            exclude_movie_ids=exclude_movie_ids,
            limit=limit
        )

    @classmethod
    def select_user_recommend_history(cls, user_id: int) -> Optional[Recommend]:
        """
        获取用户最新的推荐历史

        Args:
            user_id (int): 用户ID

        Returns:
            Optional[Recommend]: 最新的推荐记录
        """
        try:
            stmt = select(RecommendPo).where(
                RecommendPo.user_id == user_id
            ).order_by(RecommendPo.create_time.desc()).limit(1)

            result = db.session.execute(stmt).scalar_one_or_none()
            return Recommend.model_validate(result) if result else None
        except Exception as e:
            print(f"获取用户推荐历史出错: {e}")
            return None
