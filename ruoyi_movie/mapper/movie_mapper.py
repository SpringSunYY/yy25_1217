# -*- coding: utf-8 -*-
# @Author  : YY
# @FileName: movie_mapper.py
# @Time    : 2025-12-21 18:49:53

import re
from datetime import datetime
from typing import List, Optional

from flask import g
from sqlalchemy import select, delete, and_, or_, desc, asc, func

from ruoyi_admin.ext import db
from ruoyi_common.utils.base import LogUtil
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
    def select_movie_by_movie_id(movie_id: int) -> Optional[Movie]:
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
    def _build_person_search_condition(column, search_term: str):
        """
        构建人名搜索条件，支持中英文混合搜索

        Args:
            column: 数据库列
            search_term: 搜索词

        Returns:
            搜索条件
        """
        if not search_term or not search_term.strip():
            return None

        search_term = search_term.strip()
        conditions = []

        # 1. 原始搜索词的完整匹配 - 最基本的匹配
        conditions.append(column.like("%" + search_term + "%"))

        # 2. 处理中文人名 - 更宽泛的匹配
        import re
        if re.search(r'[\u4e00-\u9fff]', search_term):
            # 去除所有标点符号的版本
            clean_term = re.sub(r'[·•・\s\-\._\(\)\[\]\{\}《》""''「」]+', '', search_term)
            if clean_term != search_term and len(clean_term) > 1:
                conditions.append(column.like("%" + clean_term + "%"))

            # 将中文标点替换为空格或通配符
            relaxed_term = re.sub(r'[·•・]', ' ', search_term)
            if relaxed_term != search_term:
                conditions.append(column.like("%" + relaxed_term + "%"))

            # 更激进的匹配：允许标点处有任意字符
            wildcard_term = re.sub(r'[·•・]', '%', search_term)
            if wildcard_term != search_term:
                conditions.append(column.like("%" + wildcard_term + "%"))

        # 3. 通用分词处理 - 对所有搜索词都进行分词
        separators = r'[\s·•・\-_\.\(\)\[\]\{\}《》""''「」\u00b7\u2027\u30fb]+'
        words = re.split(separators, search_term)

        # 过滤掉空字符串和单字符
        words = [word.strip() for word in words if word.strip() and len(word.strip()) > 1]

        if len(words) > 1:
            # OR条件：只要匹配任意一个分词即可 - 更宽松
            for word in words:
                conditions.append(column.like("%" + word + "%"))

            # AND条件：所有分词都要匹配 - 更精确
            if len(words) <= 3:  # 避免分词太多导致的性能问题
                from sqlalchemy import and_
                word_conditions = [column.like("%" + word + "%") for word in words]
                conditions.append(and_(*word_conditions))

        # 4. 特殊处理：如果是两个词，尝试各种组合
        if len(words) == 2:
            word1, word2 = words[0], words[1]

            # word1在前，word2在后（中间允许任意字符）
            conditions.append(column.like("%" + word1 + "%" + word2 + "%"))

            # word2在前，word1在后
            conditions.append(column.like("%" + word2 + "%" + word1 + "%"))

            # 英文人名的特殊处理：如果是英文，尝试忽略大小写
            if re.search(r'[a-zA-Z]', word1) and re.search(r'[a-zA-Z]', word2):
                # 第一个词的首字母大写版本
                if word1[0].islower():
                    capitalized1 = word1[0].upper() + word1[1:]
                    conditions.append(column.like("%" + capitalized1 + "%" + word2 + "%"))
                    conditions.append(column.like("%" + word2 + "%" + capitalized1 + "%"))

                if word2[0].islower():
                    capitalized2 = word2[0].upper() + word2[1:]
                    conditions.append(column.like("%" + word1 + "%" + capitalized2 + "%"))
                    conditions.append(column.like("%" + capitalized2 + "%" + word1 + "%"))

        return or_(*conditions) if conditions else None

    @staticmethod
    def search_movies(movie: Movie) -> List[Movie]:
        """
        电影搜索方法

        Args:
            movie (Movie): 搜索条件

        Returns:
            List[Movie]: 搜索结果列表
        """
        try:
            # 构建查询条件
            stmt = select(MoviePo)

            # 搜索条件
            if movie.title:
                title = str(movie.title).strip()
                # 电影标题搜索也使用智能匹配
                title_conditions = []

                # 1. 完整匹配
                title_conditions.append(MoviePo.title.like("%" + title + "%"))

                # 2. 如果包含中文，进行一些变体搜索
                import re
                if re.search(r'[\u4e00-\u9fff]', title):
                    # 去除常见标点和空格
                    clean_title = re.sub(r'[《》""''（）()【】\[\]「」\s]', '', title)
                    if clean_title != title:
                        title_conditions.append(MoviePo.title.like("%" + clean_title + "%"))

                    # 去除书名号等
                    no_bookmarks = re.sub(r'[《》]', '', title)
                    if no_bookmarks != title and no_bookmarks != clean_title:
                        title_conditions.append(MoviePo.title.like("%" + no_bookmarks + "%"))

                # 3. 按空格分割的词都要匹配（用于英文标题或中英文混合）
                words = title.split()
                if len(words) > 1:
                    word_conditions = []
                    for word in words:
                        word = word.strip()
                        if word:
                            word_conditions.append(MoviePo.title.like("%" + word + "%"))
                    if word_conditions:
                        title_conditions.append(and_(*word_conditions))

                stmt = stmt.where(or_(*title_conditions))

            if movie.genres:
                # 类型搜索，支持多个类型，用逗号分隔
                genres_list = [g.strip() for g in movie.genres.split(',') if g.strip()]
                if genres_list:
                    genre_conditions = []
                    for genre in genres_list:
                        genre_conditions.append(MoviePo.genres.like("%" + genre + "%"))
                    stmt = stmt.where(or_(*genre_conditions))

            if movie.country:
                # 国家地区搜索，支持多个国家，用/分隔
                countries = [c.strip() for c in movie.country.split('/') if c.strip()]
                if countries:
                    country_conditions = []
                    for country in countries:
                        country_conditions.append(MoviePo.country.like("%" + country + "%"))
                    stmt = stmt.where(or_(*country_conditions))

            # 导演搜索 - 使用简单LIKE匹配
            if movie.directors:
                stmt = stmt.where(MoviePo.directors.like("%" + str(movie.directors) + "%"))

            # 编剧搜索 - 使用简单LIKE匹配
            if movie.writers:
                stmt = stmt.where(MoviePo.writers.like("%" + str(movie.writers) + "%"))

            # 主演搜索 - 使用简单LIKE匹配
            if movie.actors:
                stmt = stmt.where(MoviePo.actors.like("%" + str(movie.actors) + "%"))

            # 年份筛选 - 支持范围查询
            year_start = getattr(movie, 'publish_year_start', None)
            year_end = getattr(movie, 'publish_year_end', None)
            publish_year = getattr(movie, 'publish_year', None)

            if publish_year is not None:
                stmt = stmt.where(MoviePo.publish_year == publish_year)
            elif year_start is not None and year_end is not None:
                if year_start == year_end:
                    stmt = stmt.where(MoviePo.publish_year == year_start)
                else:
                    stmt = stmt.where(and_(MoviePo.publish_year >= year_start, MoviePo.publish_year <= year_end))

            # 排序
            sort_field = getattr(movie, 'sort_field', 'view_count')
            sort_order = getattr(movie, 'sort_order', 'desc')

            sort_column = None
            if sort_field == "rating":
                sort_column = MoviePo.rating
            elif sort_field == "publish_date":
                sort_column = MoviePo.publish_date
            elif sort_field == "publish_year":
                sort_column = MoviePo.publish_year
            elif sort_field == "view_count":
                sort_column = MoviePo.view_count
            else:
                sort_column = MoviePo.view_count  # 默认按看过人数排序

            if sort_order == "asc":
                stmt = stmt.order_by(asc(sort_column))
            else:
                stmt = stmt.order_by(desc(sort_column))

            # 分页处理 - 必须在最后设置page.stmt，避免监听器冲突
            if "criterian_meta" in g and g.criterian_meta.page:
                page = g.criterian_meta.page

                # 重新构建查询条件来计算总数（排除排序）
                count_stmt = select(func.count(MoviePo.id))

                # 复制所有where条件
                if movie.title:
                    title = str(movie.title).strip()
                    title_conditions = []
                    title_conditions.append(MoviePo.title.like("%" + title + "%"))
                    if re.search(r'[\u4e00-\u9fff]', title):
                        clean_title = re.sub(r'[《》""''（）()【】\[\]「」\s]', '', title)
                        if clean_title != title:
                            title_conditions.append(MoviePo.title.like("%" + clean_title + "%"))
                        no_bookmarks = re.sub(r'[《》]', '', title)
                        if no_bookmarks != title and no_bookmarks != clean_title:
                            title_conditions.append(MoviePo.title.like("%" + no_bookmarks + "%"))
                    words = title.split()
                    if len(words) > 1:
                        word_conditions = []
                        for word in words:
                            word = word.strip()
                            if word:
                                word_conditions.append(MoviePo.title.like("%" + word + "%"))
                        if word_conditions:
                            title_conditions.append(and_(*word_conditions))
                    count_stmt = count_stmt.where(or_(*title_conditions))

                if movie.genres:
                    genres_list = [g.strip() for g in movie.genres.split(',') if g.strip()]
                    if genres_list:
                        genre_conditions = []
                        for genre in genres_list:
                            genre_conditions.append(MoviePo.genres.like("%" + genre + "%"))
                        count_stmt = count_stmt.where(or_(*genre_conditions))

                if movie.country:
                    countries = [c.strip() for c in movie.country.split('/') if c.strip()]
                    if countries:
                        country_conditions = []
                        for country in countries:
                            country_conditions.append(MoviePo.country.like("%" + country + "%"))
                        count_stmt = count_stmt.where(or_(*country_conditions))

                if movie.directors:
                    count_stmt = count_stmt.where(MoviePo.directors.like("%" + str(movie.directors) + "%"))

                if movie.writers:
                    count_stmt = count_stmt.where(MoviePo.writers.like("%" + str(movie.writers) + "%"))

                if movie.actors:
                    count_stmt = count_stmt.where(MoviePo.actors.like("%" + str(movie.actors) + "%"))

                # 年份筛选
                year_start = getattr(movie, 'publish_year_start', None)
                year_end = getattr(movie, 'publish_year_end', None)
                publish_year = getattr(movie, 'publish_year', None)

                if publish_year is not None:
                    count_stmt = count_stmt.where(MoviePo.publish_year == publish_year)
                elif year_start is not None and year_end is not None:
                    if year_start == year_end:
                        count_stmt = count_stmt.where(MoviePo.publish_year == year_start)
                    else:
                        count_stmt = count_stmt.where(and_(MoviePo.publish_year >= year_start, MoviePo.publish_year <= year_end))

                try:
                    total_result = db.session.execute(count_stmt).scalar()
                    page.total = total_result or 0
                except Exception as e:
                    print(f"总数计算错误: {e}")
                    page.total = 0

                # 应用分页
                offset_val = (page.page_num - 1) * page.page_size
                stmt = stmt.offset(offset_val).limit(page.page_size)

                # 设置page.stmt用于TableResponse，但不要让监听器处理
                # page.stmt = stmt

            result = db.session.execute(stmt).scalars().all()
            return [Movie.model_validate(item) for item in result] if result else []
        except Exception as e:
            print(f"搜索电影出错: {e}")
            return []

    @staticmethod
    def get_search_options() -> dict:
        """
        获取搜索选项（类型、国家地区等）

        Returns:
            dict: 搜索选项
        """
        try:
            # 获取所有类型及其出现次数 - 按出现次数降序排序
            genre_counts = {}
            genres_stmt = select(MoviePo.genres).where(MoviePo.genres.isnot(None))
            genres_result = db.session.execute(genres_stmt).scalars().all()

            for genre_str in genres_result:
                if genre_str:
                    # 按/分割类型
                    genre_list = [g.strip() for g in genre_str.split('/') if g.strip()]
                    for genre in genre_list:
                        genre_counts[genre] = genre_counts.get(genre, 0) + 1

            # 按出现次数降序排序
            genres = sorted(genre_counts.keys(), key=lambda x: genre_counts[x], reverse=True)

            # 获取所有国家地区及其出现次数 - 按出现次数降序排序
            country_counts = {}
            countries_stmt = select(MoviePo.country).where(MoviePo.country.isnot(None))
            countries_result = db.session.execute(countries_stmt).scalars().all()

            for country_str in countries_result:
                if country_str:
                    # 按/分割国家
                    country_list = [c.strip() for c in country_str.split('/') if c.strip()]
                    for country in country_list:
                        country_counts[country] = country_counts.get(country, 0) + 1

            # 按出现次数降序排序
            countries = sorted(country_counts.keys(), key=lambda x: country_counts[x], reverse=True)

            # 年份区间选项
            year_ranges = [
                {"label": "2025-2020", "value": "2025-2020"},
                {"label": "2020-2015", "value": "2020-2015"},
                {"label": "2015-2010", "value": "2015-2010"},
                {"label": "2010-2005", "value": "2010-2005"},
                {"label": "2005-2000", "value": "2005-2000"},
                {"label": "2000-1995", "value": "2000-1995"},
                {"label": "1995-1990", "value": "1995-1990"},
                {"label": "1990-1985", "value": "1990-1985"},
                {"label": "1985-1980", "value": "1985-1980"},
                {"label": "更早", "value": "更早"}
            ]

            # 排序选项
            sort_options = [
                {"label": "热度↓", "value": "view_count_desc"},
                {"label": "热度↑", "value": "view_count_asc"},
                {"label": "评分↓", "value": "rating_desc"},
                {"label": "评分↑", "value": "rating_asc"},
                {"label": "年份↓", "value": "publish_year_desc"},
                {"label": "年份↑", "value": "publish_year_asc"}
            ]

            return {
                "genres": genres,
                "countries": countries,
                "yearRanges": year_ranges,
                "sortOptions": sort_options
            }
        except Exception as e:
            print(f"获取搜索选项出错: {e}")
            return {
                "genres": [],
                "countries": [],
                "yearRanges": [],
                "sortOptions": []
            }

    @staticmethod
    def select_similar_movies_by_dimensions(genres: str = None, directors: str = None,
                                          country: str = None, actors: str = None,
                                          exclude_movie_ids: List[int] = None,
                                          limit: Optional[int] = 20) -> List[Movie]:
        """
        根据维度信息查找相似的电影（用于推荐算法）

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
        try:
            stmt = select(MoviePo)

            # 构建相似度条件
            conditions = []

            if genres:
                # 类型匹配（支持多个类型）
                genre_list = [g.strip() for g in genres.split('/') if g.strip()]
                genre_conditions = []
                for genre in genre_list:
                    genre_conditions.append(MoviePo.genres.like(f"%{genre}%"))
                if genre_conditions:
                    conditions.append(or_(*genre_conditions))

            if directors:
                # 导演匹配
                director_list = [d.strip() for d in directors.split('/') if d.strip()]
                director_conditions = []
                for director in director_list:
                    director_conditions.append(MoviePo.directors.like(f"%{director}%"))
                if director_conditions:
                    conditions.append(or_(*director_conditions))

            if country:
                # 国家地区匹配
                country_list = [c.strip() for c in country.split('/') if c.strip()]
                country_conditions = []
                for country_item in country_list:
                    country_conditions.append(MoviePo.country.like(f"%{country_item}%"))
                if country_conditions:
                    conditions.append(or_(*country_conditions))

            if actors:
                # 主演匹配
                actor_list = [a.strip() for a in actors.split('/') if a.strip()]
                actor_conditions = []
                for actor in actor_list:
                    actor_conditions.append(MoviePo.actors.like(f"%{actor}%"))
                if actor_conditions:
                    conditions.append(or_(*actor_conditions))

            # 如果有条件，则应用条件；如果没有条件，返回热门电影
            if conditions:
                stmt = stmt.where(or_(*conditions))

            # 排除指定电影
            if exclude_movie_ids:
                stmt = stmt.where(MoviePo.movie_id.not_in(exclude_movie_ids))

            # 按评分和观看人数排序
            stmt = stmt.order_by(
                MoviePo.rating.desc(),
                MoviePo.view_count.desc()
            )

            # 只有当limit不为None时才应用限制
            if limit is not None:
                stmt = stmt.limit(limit)

            result = db.session.execute(stmt).scalars().all()
            return [Movie.model_validate(item) for item in result] if result else []
        except Exception as e:
            print(f"查找相似电影出错: {e}")
            return []

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

    @classmethod
    def select_movies_by_ids(cls, movie_ids: List[int]) -> List[Movie]:
        """
        根据电影ID列表批量查询电影信息

        Args:
            movie_ids (List[int]): 电影ID列表

        Returns:
            List[Movie]: 电影对象列表
        """
        if not movie_ids:
            return []

        try:
            # 使用SQLAlchemy的select语句
            stmt = select(MoviePo).where(MoviePo.movie_id.in_(movie_ids))

            # 保持ID顺序
            id_to_index = {movie_id: index for index, movie_id in enumerate(movie_ids)}
            result = db.session.execute(stmt).scalars().all()

            # 转换为Movie实体并按原始顺序排序
            movies = [Movie.model_validate(item) for item in result] if result else []
            movies.sort(key=lambda x: id_to_index.get(x.movie_id, len(movie_ids)))

            return movies
        except Exception as e:
            LogUtil.logger.error(f"批量查询电影信息失败: {e}")
            return []
