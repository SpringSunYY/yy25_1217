# -*- coding: utf-8 -*-
# @Author  : YY
# @FileName: movie_service.py
# @Time    : 2025-12-21 18:49:53

import re
from typing import List
from datetime import datetime

from ruoyi_common.exception import ServiceException
from ruoyi_common.utils.base import LogUtil
from ruoyi_movie.domain.entity import Movie
from ruoyi_movie.mapper.movie_mapper import MovieMapper

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

                # 处理上映日期，提取第一个日期
                if movie.pub_date:
                    first_date, publish_year = MovieService._parse_pub_date(movie.pub_date)
                    if first_date:
                        movie.pub_date = first_date
                        movie.publish_year = publish_year
                        # 同时设置publish_date（datetime类型）
                        try:
                            movie.publish_date = datetime.strptime(first_date, '%Y-%m-%d')
                        except ValueError:
                            LogUtil.logger.warning(f"无法解析日期格式: {first_date}")

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
    

    def insert_movie(self, movie: Movie) -> int:
        """
        新增电影信息表

        Args:
            movie (movie): 电影信息表对象

        Returns:
            int: 插入的记录数
        """
        return MovieMapper.insert_movie(movie)

    
    def update_movie(self, movie: Movie) -> int:
        """
        修改电影信息表

        Args:
            movie (movie): 电影信息表对象

        Returns:
            int: 更新的记录数
        """
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