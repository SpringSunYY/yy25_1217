# -*- coding: utf-8 -*-
# @Author  : YY
# @FileName: movie_service.py
# @Time    : 2025-12-21 18:49:53

from typing import List

from ruoyi_common.exception import ServiceException
from ruoyi_common.utils.base import LogUtil
from ruoyi_movie.domain.entity import Movie
from ruoyi_movie.mapper.movie_mapper import MovieMapper

class MovieService:
    """电影信息表服务类"""

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

        success_count = 0
        fail_count = 0
        success_msg = ""
        fail_msg = ""

        for movie in movie_list:
            try:
                display_value = movie
                
                display_value = getattr(movie, "id", display_value)
                existing = None
                if movie.id is not None:
                    existing = MovieMapper.select_movie_by_id(movie.id)
                if existing:
                    if is_update:
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