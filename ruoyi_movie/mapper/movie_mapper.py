# -*- coding: utf-8 -*-
# @Author  : YY
# @FileName: movie_mapper.py
# @Time    : 2025-12-21 18:49:53

from typing import List
from datetime import datetime

from flask import g
from sqlalchemy import select, update, delete

from ruoyi_admin.ext import db
from ruoyi_movie.domain.entity import Movie
from ruoyi_movie.domain.po import MoviePo

class MovieMapper:
    """电影信息表Mapper"""

    @staticmethod
    def select_movie_list(movie: Movie) -> List[Movie]:
        """
        查询电影信息表列表

        Args:
            movie (movie): 电影信息表对象

        Returns:
            List[movie]: 电影信息表列表
        """
        try:
            # 构建查询条件
            stmt = select(MoviePo)


            if movie.id is not None:
                stmt = stmt.where(MoviePo.id == movie.id)



            if movie.movie_id is not None:
                stmt = stmt.where(MoviePo.movie_id == movie.movie_id)



            if movie.title:
                stmt = stmt.where(MoviePo.title.like("%" + str(movie.title) + "%"))



            if movie.rating is not None:
                stmt = stmt.where(MoviePo.rating == movie.rating)









            if movie.language:
                stmt = stmt.where(MoviePo.language.like("%" + str(movie.language) + "%"))



            if movie.country:
                stmt = stmt.where(MoviePo.country.like("%" + str(movie.country) + "%"))



            if movie.directors:
                stmt = stmt.where(MoviePo.directors.like("%" + str(movie.directors) + "%"))



            if movie.writers:
                stmt = stmt.where(MoviePo.writers.like("%" + str(movie.writers) + "%"))



            if movie.actors:
                stmt = stmt.where(MoviePo.actors.like("%" + str(movie.actors) + "%"))









            _params = getattr(movie, "params", {}) or {}
            begin_val = _params.get("beginPublishDate")
            end_val = _params.get("endPublishDate")
            if begin_val is not None:
                stmt = stmt.where(MoviePo.publish_date >= begin_val)
            if end_val is not None:
                stmt = stmt.where(MoviePo.publish_date <= end_val)



            if movie.publish_year is not None:
                stmt = stmt.where(MoviePo.publish_year == movie.publish_year)



            if movie.genres:
                stmt = stmt.where(MoviePo.genres.like("%" + str(movie.genres) + "%"))








            if "criterian_meta" in g and g.criterian_meta.page:
                g.criterian_meta.page.stmt = stmt

            result = db.session.execute(stmt).scalars().all()
            return [Movie.model_validate(item) for item in result] if result else []
        except Exception as e:
            print(f"查询电影信息表列表出错: {e}")
            return []

    
    @staticmethod
    def select_movie_by_id(id: int) -> Movie:
        """
        根据ID查询电影信息表

        Args:
            id (int): 编号

        Returns:
            movie: 电影信息表对象
        """
        try:
            result = db.session.get(MoviePo, id)
            return Movie.model_validate(result) if result else None
        except Exception as e:
            print(f"根据ID查询电影信息表出错: {e}")
            return None

    @staticmethod
    def select_movie_by_movie_id(movie_id: int) -> Movie:
        """
        根据电影ID查询电影信息表

        Args:
            movie_id (int): 电影ID

        Returns:
            movie: 电影信息表对象
        """
        try:
            stmt = select(MoviePo).where(MoviePo.movie_id == movie_id)
            result = db.session.execute(stmt).scalar_one_or_none()
            return Movie.model_validate(result) if result else None
        except Exception as e:
            print(f"根据电影ID查询电影信息表出错: {e}")
            return None
    

    @staticmethod
    def insert_movie(movie: Movie) -> int:
        """
        新增电影信息表

        Args:
            movie (movie): 电影信息表对象

        Returns:
            int: 插入的记录数
        """
        try:
            now = datetime.now()
            new_po = MoviePo()
            # id字段由数据库自动生成，不手动设置
            new_po.movie_id = movie.movie_id
            new_po.title = movie.title
            new_po.rating = movie.rating
            new_po.view_count = movie.view_count
            new_po.wish_count = movie.wish_count
            new_po.reviews_count = movie.reviews_count
            new_po.language = movie.language
            new_po.country = movie.country
            new_po.directors = movie.directors
            new_po.writers = movie.writers
            new_po.actors = movie.actors
            new_po.duration = movie.duration
            new_po.duration_minute = movie.duration_minute
            new_po.pub_date = movie.pub_date
            new_po.publish_date = movie.publish_date
            new_po.publish_year = movie.publish_year
            new_po.genres = movie.genres
            new_po.summary = movie.summary
            new_po.cover_url = movie.cover_url
            new_po.detail_url = movie.detail_url
            db.session.add(new_po)
            db.session.commit()
            movie.id = new_po.id
            return 1
        except Exception as e:
            db.session.rollback()
            print(f"新增电影信息表出错: {e}")
            return 0

    
    @staticmethod
    def update_movie(movie: Movie) -> int:
        """
        修改电影信息表

        Args:
            movie (movie): 电影信息表对象

        Returns:
            int: 更新的记录数
        """
        try:
            
            existing = db.session.get(MoviePo, movie.id)
            if not existing:
                return 0
            now = datetime.now()
            # 主键不参与更新
            existing.movie_id = movie.movie_id
            existing.title = movie.title
            existing.rating = movie.rating
            existing.view_count = movie.view_count
            existing.wish_count = movie.wish_count
            existing.reviews_count = movie.reviews_count
            existing.language = movie.language
            existing.country = movie.country
            existing.directors = movie.directors
            existing.writers = movie.writers
            existing.actors = movie.actors
            existing.duration = movie.duration
            existing.duration_minute = movie.duration_minute
            existing.pub_date = movie.pub_date
            existing.publish_date = movie.publish_date
            existing.publish_year = movie.publish_year
            existing.genres = movie.genres
            existing.summary = movie.summary
            existing.cover_url = movie.cover_url
            existing.detail_url = movie.detail_url
            db.session.commit()
            return 1
            
        except Exception as e:
            db.session.rollback()
            print(f"修改电影信息表出错: {e}")
            return 0

    @staticmethod
    def delete_movie_by_ids(ids: List[int]) -> int:
        """
        批量删除电影信息表

        Args:
            ids (List[int]): ID列表

        Returns:
            int: 删除的记录数
        """
        try:
            stmt = delete(MoviePo).where(MoviePo.id.in_(ids))
            result = db.session.execute(stmt)
            db.session.commit()
            return result.rowcount
        except Exception as e:
            db.session.rollback()
            print(f"批量删除电影信息表出错: {e}")
            return 0
    