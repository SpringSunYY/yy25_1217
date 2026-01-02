# -*- coding: utf-8 -*-
# @Author  : YY
# @FileName: view_service.py
# @Time    : 2025-12-21 18:49:52
from datetime import datetime
from typing import List

from ruoyi_common.exception import ServiceException
from ruoyi_common.utils.base import LogUtil
from ruoyi_common.utils.security_util import get_user_id, get_username
from ruoyi_movie.domain.entity import View, Movie
from ruoyi_movie.mapper.view_mapper import ViewMapper


class ViewService:
    """用户浏览服务类"""

    def select_view_list(self, view: View) -> List[View]:
        """
        查询用户浏览列表

        Args:
            view (view): 用户浏览对象

        Returns:
            List[view]: 用户浏览列表
        """
        return ViewMapper.select_view_list(view)

    def select_view_by_id(self, id: int) -> View:
        """
        根据ID查询用户浏览

        Args:
            id (int): 浏览编号

        Returns:
            view: 用户浏览对象
        """
        return ViewMapper.select_view_by_id(id)

    def insert_view(self, view: View) -> int:
        """
        新增用户浏览

        Args:
            view (view): 用户浏览对象

        Returns:
            int: 插入的记录数
        """
        return ViewMapper.insert_view(view)

    @staticmethod
    def add_view(movie: Movie) -> int:
        """
        添加用户浏览记录

        Args:
            movie (Movie): 添加的movie对象
        """
        view_info = View()
        ##首先查询用户今天是否已经看过此电影
        now_date = datetime.now()
        user_id = get_user_id()
        existing = ViewMapper.select_view_by_movie_id_and_date(movie.movie_id, user_id, now_date)
        if existing:
            return 0
        view_info.user_id = user_id
        view_info.user_name = get_username()
        view_info.movie_id = movie.movie_id
        view_info.movie_title = movie.title
        view_info.cover_url = movie.cover_url
        view_info.genres = movie.genres
        view_info.directors = movie.directors
        view_info.country = movie.country
        view_info.actors = movie.actors
        view_info.score = 1
        view_info.create_time = now_date
        return ViewMapper.insert_view(view_info)

    def update_view(self, view: View) -> int:
        """
        修改用户浏览

        Args:
            view (view): 用户浏览对象

        Returns:
            int: 更新的记录数
        """
        return ViewMapper.update_view(view)

    def delete_view_by_ids(self, ids: List[int]) -> int:
        """
        批量删除用户浏览

        Args:
            ids (List[int]): ID列表

        Returns:
            int: 删除的记录数
        """
        return ViewMapper.delete_view_by_ids(ids)

    def import_view(self, view_list: List[View], is_update: bool = False) -> str:
        """
        导入用户浏览数据

        Args:
            view_list (List[view]): 用户浏览列表
            is_update (bool): 是否更新已存在的数据

        Returns:
            str: 导入结果消息
        """
        if not view_list:
            raise ServiceException("导入用户浏览数据不能为空")

        success_count = 0
        fail_count = 0
        success_msg = ""
        fail_msg = ""

        for view in view_list:
            try:
                display_value = view

                display_value = getattr(view, "id", display_value)
                existing = None
                if view.id is not None:
                    existing = ViewMapper.select_view_by_id(view.id)
                if existing:
                    if is_update:
                        result = ViewMapper.update_view(view)
                    else:
                        fail_count += 1
                        fail_msg += f"<br/> 第{fail_count}条数据，已存在：{display_value}"
                        continue
                else:
                    result = ViewMapper.insert_view(view)

                if result > 0:
                    success_count += 1
                    success_msg += f"<br/> 第{success_count}条数据，操作成功：{display_value}"
                else:
                    fail_count += 1
                    fail_msg += f"<br/> 第{fail_count}条数据，操作失败：{display_value}"
            except Exception as e:
                fail_count += 1
                fail_msg += f"<br/> 第{fail_count}条数据，导入失败，原因：{e.__class__.__name__}"
                LogUtil.logger.error(f"导入用户浏览失败，原因：{e}")

        if fail_count > 0:
            if success_msg:
                fail_msg = f"导入成功{success_count}条，失败{fail_count}条。{success_msg}<br/>" + fail_msg
            else:
                fail_msg = f"导入成功{success_count}条，失败{fail_count}条。{fail_msg}"
            raise ServiceException(fail_msg)
        success_msg = f"恭喜您，数据已全部导入成功！共 {success_count} 条，数据如下：" + success_msg
        return success_msg
