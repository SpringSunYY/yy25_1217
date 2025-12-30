# -*- coding: utf-8 -*-
# @Author  : YY
# @FileName: movie_review_mapper.py
# @Time    : 2025-12-30 17:06:59

from datetime import datetime
from typing import List

from flask import g
from sqlalchemy import select, delete

from ruoyi_admin.ext import db
from ruoyi_movie.domain.entity import MovieReview
from ruoyi_movie.domain.po import MovieReviewPo

class MovieReviewMapper:
    """影评信息表Mapper"""

    @staticmethod
    def select_movie_review_list(movie_review: MovieReview) -> List[MovieReview]:
        """
        查询影评信息表列表

        Args:
            movie_review (movie_review): 影评信息表对象

        Returns:
            List[movie_review]: 影评信息表列表
        """
        try:
            # 构建查询条件
            stmt = select(MovieReviewPo)

            if movie_review.id is not None:
                stmt = stmt.where(MovieReviewPo.id == movie_review.id)

            if movie_review.review_id is not None:
                stmt = stmt.where(MovieReviewPo.review_id == movie_review.review_id)

            if movie_review.movie_id is not None:
                stmt = stmt.where(MovieReviewPo.movie_id == movie_review.movie_id)

            if movie_review.type is not None:
                stmt = stmt.where(MovieReviewPo.type == movie_review.type)

            if movie_review.user_name:
                stmt = stmt.where(MovieReviewPo.user_name.like("%" + str(movie_review.user_name) + "%"))

            if movie_review.rating_star is not None:
                stmt = stmt.where(MovieReviewPo.rating_star == movie_review.rating_star)

            _params = getattr(movie_review, "params", {}) or {}
            begin_val = _params.get("beginCommentTime")
            end_val = _params.get("endCommentTime")
            if begin_val is not None:
                stmt = stmt.where(MovieReviewPo.comment_time >= begin_val)
            if end_val is not None:
                stmt = stmt.where(MovieReviewPo.comment_time <= end_val)

            if movie_review.review_title:
                stmt = stmt.where(MovieReviewPo.review_title.like("%" + str(movie_review.review_title) + "%"))

            if "criterian_meta" in g and g.criterian_meta.page:
                g.criterian_meta.page.stmt = stmt

            result = db.session.execute(stmt).scalars().all()
            return [MovieReview.model_validate(item) for item in result] if result else []
        except Exception as e:
            print(f"查询影评信息表列表出错: {e}")
            return []

    @staticmethod
    def select_movie_review_by_id(id: int) -> MovieReview:
        """
        根据ID查询影评信息表

        Args:
            id (int): 编号

        Returns:
            movie_review: 影评信息表对象
        """
        try:
            stmt = select(MovieReviewPo).where(MovieReviewPo.id == id)
            result = db.session.execute(stmt).scalar_one_or_none()
            return MovieReview.model_validate(result) if result else None
        except Exception as e:
            print(f"根据ID查询影评信息表出错: {e}")
            return None

    @staticmethod
    def select_movie_review_by_review_id(review_id) -> MovieReview:
        try:
            stmt = select(MovieReviewPo).where(MovieReviewPo.review_id == review_id)
            result = db.session.execute(stmt).scalar_one_or_none()
            return MovieReview.model_validate(result) if result else None
        except Exception as e:
            print(f"根据ID字段查询影评信息表出错: {e}")
        return None

    @staticmethod
    def insert_movie_review(movie_review: MovieReview) -> int:
        """
        新增影评信息表

        Args:
            movie_review (movie_review): 影评信息表对象

        Returns:
            int: 插入的记录数
        """
        try:
            now = datetime.now()
            new_po = MovieReviewPo()
            new_po.id = movie_review.id
            new_po.review_id = movie_review.review_id
            new_po.movie_id = movie_review.movie_id
            new_po.type = movie_review.type
            new_po.user_name = movie_review.user_name
            new_po.rating_star = movie_review.rating_star
            new_po.votes_up = movie_review.votes_up
            new_po.votes_down = movie_review.votes_down
            new_po.replies_count = movie_review.replies_count
            new_po.comment_time = movie_review.comment_time
            new_po.review_title = movie_review.review_title
            new_po.user_avatar = movie_review.user_avatar
            new_po.content = movie_review.content
            db.session.add(new_po)
            db.session.commit()
            movie_review.id = new_po.id
            return 1
        except Exception as e:
            db.session.rollback()
            print(f"新增影评信息表出错: {e}")
            return 0

    @staticmethod
    def update_movie_review(movie_review: MovieReview) -> int:
        """
        修改影评信息表

        Args:
            movie_review (movie_review): 影评信息表对象

        Returns:
            int: 更新的记录数
        """
        try:

            existing = db.session.get(MovieReviewPo, movie_review.id)
            if not existing:
                return 0
            now = datetime.now()
            # 主键不参与更新
            existing.review_id = movie_review.review_id
            existing.movie_id = movie_review.movie_id
            existing.type = movie_review.type
            existing.user_name = movie_review.user_name
            existing.rating_star = movie_review.rating_star
            existing.votes_up = movie_review.votes_up
            existing.votes_down = movie_review.votes_down
            existing.replies_count = movie_review.replies_count
            existing.comment_time = movie_review.comment_time
            existing.review_title = movie_review.review_title
            existing.user_avatar = movie_review.user_avatar
            existing.content = movie_review.content
            db.session.commit()
            return 1

        except Exception as e:
            db.session.rollback()
            print(f"修改影评信息表出错: {e}")
            return 0

    @staticmethod
    def delete_movie_review_by_ids(ids: List[int]) -> int:
        """
        批量删除影评信息表

        Args:
            ids (List[int]): ID列表

        Returns:
            int: 删除的记录数
        """
        try:
            stmt = delete(MovieReviewPo).where(MovieReviewPo.id.in_(ids))
            result = db.session.execute(stmt)
            db.session.commit()
            return result.rowcount
        except Exception as e:
            db.session.rollback()
            print(f"批量删除影评信息表出错: {e}")
            return 0
