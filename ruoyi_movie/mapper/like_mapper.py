# -*- coding: utf-8 -*-
# @Author  : YY
# @FileName: like_mapper.py
# @Time    : 2025-12-21 18:49:53

from typing import List, Optional
from datetime import datetime

from flask import g
from sqlalchemy import select, update, delete

from ruoyi_admin.ext import db
from ruoyi_movie.domain.entity import Like
from ruoyi_movie.domain.po import LikePo


class LikeMapper:
    """用户点赞表Mapper"""

    @staticmethod
    def select_like_list(like: Like) -> List[Like]:
        """
        查询用户点赞表列表

        Args:
            like (like): 用户点赞表对象

        Returns:
            List[like]: 用户点赞表列表
        """
        try:
            # 构建查询条件
            stmt = select(LikePo)

            if like.id is not None:
                stmt = stmt.where(LikePo.id == like.id)

            if like.user_id is not None:
                stmt = stmt.where(LikePo.user_id == like.user_id)

            if like.user_name:
                stmt = stmt.where(LikePo.user_name.like("%" + str(like.user_name) + "%"))

            if like.movie_id is not None:
                stmt = stmt.where(LikePo.movie_id == like.movie_id)

            if like.movie_title:
                stmt = stmt.where(LikePo.movie_title.like("%" + str(like.movie_title) + "%"))

            if like.genres:
                stmt = stmt.where(LikePo.genres.like("%" + str(like.genres) + "%"))

            if like.directors:
                stmt = stmt.where(LikePo.directors.like("%" + str(like.directors) + "%"))

            if like.country:
                stmt = stmt.where(LikePo.country.like("%" + str(like.country) + "%"))

            if like.actors:
                stmt = stmt.where(LikePo.actors.like("%" + str(like.actors) + "%"))

            _params = getattr(like, "params", {}) or {}
            begin_val = _params.get("beginCreateTime")
            end_val = _params.get("endCreateTime")
            if begin_val is not None:
                stmt = stmt.where(LikePo.create_time >= begin_val)
            if end_val is not None:
                stmt = stmt.where(LikePo.create_time <= end_val)

            if "criterian_meta" in g and g.criterian_meta.page:
                g.criterian_meta.page.stmt = stmt

            result = db.session.execute(stmt).scalars().all()
            return [Like.model_validate(item) for item in result] if result else []
        except Exception as e:
            print(f"查询用户点赞表列表出错: {e}")
            return []

    @staticmethod
    def select_like_by_id(id: int) -> Like:
        """
        根据ID查询用户点赞表

        Args:
            id (int): 点赞编号

        Returns:
            like: 用户点赞表对象
        """
        try:
            result = db.session.get(LikePo, id)
            return Like.model_validate(result) if result else None
        except Exception as e:
            print(f"根据ID查询用户点赞表出错: {e}")
            return None

    @staticmethod
    def insert_like(like: Like) -> int:
        """
        新增用户点赞表

        Args:
            like (like): 用户点赞表对象

        Returns:
            int: 插入的记录数
        """
        try:
            now = datetime.now()
            new_po = LikePo()
            new_po.id = like.id
            new_po.user_id = like.user_id
            new_po.user_name = like.user_name
            new_po.movie_id = like.movie_id
            new_po.movie_title = like.movie_title
            new_po.cover_url = like.cover_url
            new_po.genres = like.genres
            new_po.directors = like.directors
            new_po.country = like.country
            new_po.actors = like.actors
            new_po.score = like.score
            new_po.create_time = like.create_time or now
            db.session.add(new_po)
            db.session.commit()
            like.id = new_po.id
            return 1
        except Exception as e:
            db.session.rollback()
            print(f"新增用户点赞表出错: {e}")
            return 0

    @staticmethod
    def update_like(like: Like) -> int:
        """
        修改用户点赞表

        Args:
            like (like): 用户点赞表对象

        Returns:
            int: 更新的记录数
        """
        try:

            existing = db.session.get(LikePo, like.id)
            if not existing:
                return 0
            now = datetime.now()
            # 主键不参与更新
            existing.user_id = like.user_id
            existing.user_name = like.user_name
            existing.movie_id = like.movie_id
            existing.movie_title = like.movie_title
            existing.cover_url = like.cover_url
            existing.genres = like.genres
            existing.directors = like.directors
            existing.country = like.country
            existing.actors = like.actors
            existing.score = like.score
            existing.create_time = like.create_time
            db.session.commit()
            return 1

        except Exception as e:
            db.session.rollback()
            print(f"修改用户点赞表出错: {e}")
            return 0

    @staticmethod
    def delete_like_by_ids(ids: List[int]) -> int:
        """
        批量删除用户点赞表

        Args:
            ids (List[int]): ID列表

        Returns:
            int: 删除的记录数
        """
        try:
            stmt = delete(LikePo).where(LikePo.id.in_(ids))
            result = db.session.execute(stmt)
            db.session.commit()
            return result.rowcount
        except Exception as e:
            db.session.rollback()
            print(f"批量删除用户点赞表出错: {e}")
            return 0

    @staticmethod
    def cancel_like(like):
        """
        取消点赞

        Args:
            like (Like): 用户点赞表对象

        Returns:
            int: 删除的记录数
        """
        try:
            stmt = delete(LikePo).where(LikePo.movie_id == like.movie_id,
                                        LikePo.user_id == like.user_id);
            result = db.session.execute(stmt)
            db.session.commit()
            return result.rowcount
        except Exception as e:
            db.session.rollback()
            print(f"取消点赞出错: {e}")
            return 0
        pass

    @staticmethod
    def select_like_by_movie_id_and_user_id(movie_id, user_id) -> Optional[Like]:
        """
        根据电影ID和用户ID查询用户点赞表

        Args:
            movie_id (int): 电影ID
            user_id (int): 用户ID

        Returns:
            Like: 用户点赞表对象
        """
        try:
            result = db.session.execute(
                select(LikePo).where(LikePo.movie_id == movie_id, LikePo.user_id == user_id)).scalars().first()
            return Like.model_validate(result) if result else None
        except Exception as e:
            print(f"根据电影ID和用户ID查询用户点赞表出错: {e}")
            return None
