# -*- coding: utf-8 -*-
# @Author  : YY
# @FileName: movie_service.py
# @Time    : 2025-12-21 18:49:53

import re
from datetime import datetime
from typing import List

from ruoyi_common.exception import ServiceException
from ruoyi_common.utils.base import LogUtil
from ruoyi_common.utils.security_util import get_user_id
from ruoyi_movie.domain.entity import Movie
from ruoyi_movie.domain.entity.movie import MovieDetailDto
from ruoyi_movie.mapper import MovieReviewMapper, LikeMapper
from ruoyi_movie.mapper.movie_mapper import MovieMapper
from ruoyi_movie.service.view_service import ViewService


class MovieService:
    """电影信息表服务类"""

    @staticmethod
    def preprocess_movie_data(movie_list: List[Movie]) -> List[Movie]:
        """
        预处理电影数据

        Args:
            movie_list: 电影数据列表

        Returns:
            处理后的电影数据列表
        """
        processed_list = []

        for movie in movie_list:
            try:
                # 处理片长，提取分钟数
                if movie.duration and movie.duration != "未知":
                    duration_minute = MovieService._parse_duration_to_minutes(movie.duration)
                    if duration_minute is not None:
                        movie.duration_minute = duration_minute
                    else:
                        # 如果无法解析，跳过这条数据
                        LogUtil.logger.warning(f"无法解析片长数据: {movie.duration}，跳过该条数据")
                        continue
                elif movie.duration == "未知":
                    # 跳过未知数据
                    continue

                # 处理上映日期，提取第一个日期用于设置publish_date和publish_year
                # 注意：保持原有的pub_date字段不变
                # 必须要有有效的上映时间，否则跳过该数据
                if not movie.pub_date:
                    LogUtil.logger.warning(f"上映日期为空，跳过该条数据")
                    continue

                first_date, publish_year = MovieService._parse_pub_date(movie.pub_date)
                if first_date and publish_year:
                    # 设置上映时间（datetime类型）
                    try:
                        movie.publish_date = datetime.strptime(first_date, '%Y-%m-%d')
                        movie.publish_year = publish_year
                    except ValueError:
                        # 如果无法解析为datetime格式，跳过该数据
                        LogUtil.logger.warning(f"无法解析日期格式: {first_date}，跳过该条数据")
                        continue
                else:
                    # 如果无法提取有效的日期，跳过该数据
                    LogUtil.logger.warning(f"无法从上映日期中提取有效日期: {movie.pub_date}，跳过该条数据")
                    continue

                processed_list.append(movie)

            except Exception as e:
                LogUtil.logger.error(f"预处理电影数据出错: {e}")
                continue

        return processed_list

    @staticmethod
    def _parse_duration_to_minutes(duration_str: str) -> int | None:
        """
        解析片长字符串为分钟数

        Args:
            duration_str: 片长字符串，如 "141分钟"

        Returns:
            分钟数或None
        """
        if not duration_str:
            return None

        # 使用正则表达式提取数字
        match = re.search(r'(\d+)', duration_str)
        if match:
            return int(match.group(1))
        return None

    @staticmethod
    def _parse_pub_date(pub_date_str: str) -> tuple[str | None, int | None]:
        """
        解析上映日期字符串，提取第一个日期和年份

        Args:
            pub_date_str: 上映日期字符串，如 "2024-06-08(中国大陆)/2024-04-19(北京国际电影节)"

        Returns:
            (第一个日期, 年份) 或 (None, None)
        """
        if not pub_date_str:
            return None, None

        # 使用正则表达式提取第一个日期
        date_match = re.search(r'(\d{4}-\d{2}-\d{2})', pub_date_str)
        if date_match:
            first_date = date_match.group(1)
            try:
                # 提取年份
                year = int(first_date[:4])
                return first_date, year
            except ValueError:
                pass

        return None, None

    def select_movie_list(self, movie: Movie) -> List[Movie]:
        """
        查询电影信息表列表

        Args:
            movie (movie): 电影信息表对象

        Returns:
            List[movie]: 电影信息表列表
        """
        return MovieMapper.select_movie_list(movie)

    def select_movie_by_id(self, id: int) -> Movie:
        """
        根据ID查询电影信息表

        Args:
            id (int): 编号

        Returns:
            movie: 电影信息表对象
        """
        return MovieMapper.select_movie_by_id(id)

    def select_movie_detail_by_id(self, movie_id) -> MovieDetailDto:
        """
        根据电影编号查询电影信息
        Args:
            movie_id:

        Returns:

        """
        movie_detail = MovieDetailDto()
        ##首先查询电影信息
        movie_info = MovieMapper.select_movie_by_movie_id(movie_id)

        ##如果电影信息存在
        if movie_info is not None:
            movie_detail.movie = movie_info
            ##添加用户浏览记录
            ViewService.add_view(movie_info)
            ##查询用户是否点赞
            likes = LikeMapper.select_like_by_movie_id_and_user_id(movie_id, get_user_id())
            if likes:
                movie_detail.is_liked = True
            else:
                movie_detail.is_liked = False
        movie_reviews = MovieReviewMapper.select_movie_review_by_movie_id(movie_id)
        if movie_reviews:
            movie_detail.movie_review = movie_reviews
        return movie_detail

    def insert_movie(self, movie: Movie) -> int:
        """
        新增电影信息表

        Args:
            movie (movie): 电影信息表对象

        Returns:
            int: 插入的记录数
        """
        # 首先查询是否已存在
        existing = MovieMapper.select_movie_by_movie_id(movie.movie_id)
        if existing:
            raise ServiceException("已存在该电影")
        return MovieMapper.insert_movie(movie)

    def update_movie(self, movie: Movie) -> int:
        """
        修改电影信息表

        Args:
            movie (movie): 电影信息表对象

        Returns:
            int: 更新的记录数
        """
        existing = MovieMapper.select_movie_by_movie_id(movie.movie_id)
        if not existing:
            raise ServiceException("不存在该电影")
        if movie.id != existing.id:
            raise ServiceException("该电影编号已存在，不可修为此编号")
        return MovieMapper.update_movie(movie)

    def delete_movie_by_ids(self, ids: List[int]) -> int:
        """
        批量删除电影信息表

        Args:
            ids (List[int]): ID列表

        Returns:
            int: 删除的记录数
        """
        return MovieMapper.delete_movie_by_ids(ids)

    def search_movies(self, search_dto) -> List[Movie]:
        """
        电影搜索方法

        Args:
            search_dto: 搜索条件DTO

        Returns:
            List[Movie]: 搜索结果列表
        """
        # 构建Movie实体作为查询条件
        movie_entity = Movie()

        # 转换搜索条件
        for attr in ['title', 'genres', 'country', 'directors', 'writers', 'actors']:
            if hasattr(search_dto, attr) and getattr(search_dto, attr):
                setattr(movie_entity, attr, getattr(search_dto, attr))

        # 处理年份区间筛选
        if hasattr(search_dto, 'year_range') and search_dto.year_range:
            year_ranges = {
                "2025-2020": (2020, 2025),
                "2020-2015": (2015, 2020),
                "2015-2010": (2010, 2015),
                "2010-2005": (2005, 2010),
                "2005-2000": (2000, 2005),
                "2000-1995": (1995, 2000),
                "1995-1990": (1990, 1995),
                "1990-1985": (1985, 1990),
                "1985-1980": (1980, 1985),
                "更早": (0, 1980)
            }
            if search_dto.year_range in year_ranges:
                start_year, end_year = year_ranges[search_dto.year_range]
                # 设置年份范围查询条件
                setattr(movie_entity, 'publish_year_start', start_year)
                setattr(movie_entity, 'publish_year_end', end_year)
            else:
                # 如果是具体年份
                try:
                    year = int(search_dto.year_range)
                    setattr(movie_entity, 'publish_year', year)
                except:
                    pass

        # 处理排序参数
        if hasattr(search_dto, 'sort_field') and hasattr(search_dto, 'sort_order'):
            setattr(movie_entity, 'sort_field', search_dto.sort_field)
            setattr(movie_entity, 'sort_order', search_dto.sort_order)

        return MovieMapper.search_movies(movie_entity)

    def get_search_options(self) -> dict:
        """
        获取搜索选项（类型、国家地区等）

        Returns:
            dict: 搜索选项
        """
        return MovieMapper.get_search_options()

    def import_movie(self, movie_list: List[Movie], is_update: bool = False) -> str:
        """
        导入电影信息表数据

        Args:
            movie_list (List[movie]): 电影信息表列表
            is_update (bool): 是否更新已存在的数据

        Returns:
            str: 导入结果消息
        """
        if not movie_list:
            raise ServiceException("导入电影信息表数据不能为空")

        # 预处理数据
        movie_list = self.preprocess_movie_data(movie_list)

        if not movie_list:
            raise ServiceException("预处理后没有有效数据")

        success_count = 0
        fail_count = 0
        success_msg = ""
        fail_msg = ""

        for movie in movie_list:
            try:
                display_value = getattr(movie, "title", "未知电影") or getattr(movie, "movie_id", "未知ID")

                # 使用movie_id作为唯一键来检查是否存在
                existing = None
                if movie.movie_id is not None:
                    # 需要添加一个根据movie_id查询的方法
                    existing_movie = MovieMapper.select_movie_by_movie_id(movie.movie_id)
                    existing = existing_movie

                if existing:
                    if is_update:
                        # 更新时需要设置正确的id
                        movie.id = existing.id
                        result = MovieMapper.update_movie(movie)
                    else:
                        fail_count += 1
                        fail_msg += f"<br/> 第{fail_count}条数据，已存在：{display_value}"
                        continue
                else:
                    result = MovieMapper.insert_movie(movie)

                if result > 0:
                    success_count += 1
                    success_msg += f"<br/> 第{success_count}条数据，操作成功：{display_value}"
                else:
                    fail_count += 1
                    fail_msg += f"<br/> 第{fail_count}条数据，操作失败：{display_value}"
            except Exception as e:
                fail_count += 1
                fail_msg += f"<br/> 第{fail_count}条数据，导入失败，原因：{e.__class__.__name__}"
                LogUtil.logger.error(f"导入电影信息表失败，原因：{e}")

        if fail_count > 0:
            if success_msg:
                fail_msg = f"导入成功{success_count}条，失败{fail_count}条。{success_msg}<br/>" + fail_msg
            else:
                fail_msg = f"导入成功{success_count}条，失败{fail_count}条。{fail_msg}"
            raise ServiceException(fail_msg)
        success_msg = f"恭喜您，数据已全部导入成功！共 {success_count} 条，数据如下：" + success_msg
        return success_msg
