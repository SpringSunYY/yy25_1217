# -*- coding: utf-8 -*-
# @Author  : YY
# @FileName: view_mapper.py
# @Time    : 2025-12-21 18:49:52

from typing import List
from datetime import datetime, date

from flask import g
from sqlalchemy import select, update, delete

from ruoyi_admin.ext import db
from ruoyi_movie.domain.entity import View
from ruoyi_movie.domain.po import ViewPo


class ViewMapper:
    """用户浏览Mapper"""

    @staticmethod
    def select_view_list(view: View) -> List[View]:
        """
        查询用户浏览列表

        Args:
            view (view): 用户浏览对象

        Returns:
            List[view]: 用户浏览列表
        """
        try:
            # 构建查询条件
            stmt = select(ViewPo)

            if view.id is not None:
                stmt = stmt.where(ViewPo.id == view.id)

            if view.user_name:
                stmt = stmt.where(ViewPo.user_name.like("%" + str(view.user_name) + "%"))

            if view.movie_title:
                stmt = stmt.where(ViewPo.movie_title.like("%" + str(view.movie_title) + "%"))

            if view.genres:
                stmt = stmt.where(ViewPo.genres.like("%" + str(view.genres) + "%"))

            if view.directors:
                stmt = stmt.where(ViewPo.directors.like("%" + str(view.directors) + "%"))

            if view.country:
                stmt = stmt.where(ViewPo.country.like("%" + str(view.country) + "%"))

            if view.actors:
                stmt = stmt.where(ViewPo.actors.like("%" + str(view.actors) + "%"))

            _params = getattr(view, "params", {}) or {}
            begin_val = _params.get("beginCreateTime")
            end_val = _params.get("endCreateTime")
            if begin_val is not None:
                stmt = stmt.where(ViewPo.create_time >= begin_val)
            if end_val is not None:
                stmt = stmt.where(ViewPo.create_time <= end_val)

            if "criterian_meta" in g and g.criterian_meta.page:
                g.criterian_meta.page.stmt = stmt

            result = db.session.execute(stmt).scalars().all()
            return [View.model_validate(item) for item in result] if result else []
        except Exception as e:
            print(f"查询用户浏览列表出错: {e}")
            return []

    @staticmethod
    def select_view_by_id(id: int) -> View:
        """
        根据ID查询用户浏览

        Args:
            id (int): 浏览编号

        Returns:
            view: 用户浏览对象
        """
        try:
            result = db.session.get(ViewPo, id)
            return View.model_validate(result) if result else None
        except Exception as e:
            print(f"根据ID查询用户浏览出错: {e}")
            return None

    @staticmethod
    def insert_view(view: View) -> int:
        """
        新增用户浏览

        Args:
            view (view): 用户浏览对象

        Returns:
            int: 插入的记录数
        """
        try:
            now = datetime.now()
            new_po = ViewPo()
            new_po.id = view.id
            new_po.user_id = view.user_id
            new_po.user_name = view.user_name
            new_po.movie_id = view.movie_id
            new_po.movie_title = view.movie_title
            new_po.cover_url = view.cover_url
            new_po.genres = view.genres
            new_po.directors = view.directors
            new_po.country = view.country
            new_po.actors = view.actors
            new_po.score = view.score
            new_po.create_time = view.create_time or now
            db.session.add(new_po)
            db.session.commit()
            view.id = new_po.id
            return 1
        except Exception as e:
            db.session.rollback()
            print(f"新增用户浏览出错: {e}")
            return 0

    @staticmethod
    def update_view(view: View) -> int:
        """
        修改用户浏览

        Args:
            view (view): 用户浏览对象

        Returns:
            int: 更新的记录数
        """
        try:

            existing = db.session.get(ViewPo, view.id)
            if not existing:
                return 0
            now = datetime.now()
            # 主键不参与更新
            existing.user_id = view.user_id
            existing.user_name = view.user_name
            existing.movie_id = view.movie_id
            existing.movie_title = view.movie_title
            existing.cover_url = view.cover_url
            existing.genres = view.genres
            existing.directors = view.directors
            existing.country = view.country
            existing.actors = view.actors
            existing.score = view.score
            existing.create_time = view.create_time
            db.session.commit()
            return 1

        except Exception as e:
            db.session.rollback()
            print(f"修改用户浏览出错: {e}")
            return 0

    @staticmethod
    def delete_view_by_ids(ids: List[int]) -> int:
        """
        批量删除用户浏览

        Args:
            ids (List[int]): ID列表

        Returns:
            int: 删除的记录数
        """
        try:
            stmt = delete(ViewPo).where(ViewPo.id.in_(ids))
            result = db.session.execute(stmt)
            db.session.commit()
            return result.rowcount
        except Exception as e:
            db.session.rollback()
            print(f"批量删除用户浏览出错: {e}")
            return 0

    @staticmethod
    def select_view_by_movie_id_and_date(movie_id: int, user_id: int, target_date: datetime):
        """
        根据用户和时间
        Args:
            movie_id:
            user_id:
            target_date:

        Returns:
                    """

        try:
            # 如果没有提供目标日期，则使用今天
            if target_date is None:
                target_date = date.today()

            # 将年月日转换为当天的开始时间(00:00:00)和结束时间(23:59:59)
            start_of_day = datetime.combine(target_date, datetime.min.time())
            end_of_day = datetime.combine(target_date, datetime.max.time())

            stmt = select(ViewPo).where(
                ViewPo.movie_id == movie_id,
                ViewPo.user_id == user_id,
                # 按年月日范围查询评论
                ViewPo.create_time >= start_of_day,
                ViewPo.create_time <= end_of_day
            )
            result = db.session.execute(stmt).scalars().all()
            return [View.model_validate(item) for item in result] if result else []
        except Exception as e:
            print(f"根据电影ID查询影评信息表出错: {e}")
            return []
        pass
