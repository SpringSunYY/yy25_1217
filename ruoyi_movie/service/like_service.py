# -*- coding: utf-8 -*-
# @Author  : YY
# @FileName: like_service.py
# @Time    : 2025-12-21 18:49:53

from typing import List

from ruoyi_common.exception import ServiceException
from ruoyi_common.utils.base import LogUtil
from ruoyi_movie.domain.entity import Like
from ruoyi_movie.mapper.like_mapper import LikeMapper

class LikeService:
    """用户点赞表服务类"""

    def select_like_list(self, like: Like) -> List[Like]:
        """
        查询用户点赞表列表

        Args:
            like (like): 用户点赞表对象

        Returns:
            List[like]: 用户点赞表列表
        """
        return LikeMapper.select_like_list(like)

    
    def select_like_by_id(self, id: int) -> Like:
        """
        根据ID查询用户点赞表

        Args:
            id (int): 点赞编号

        Returns:
            like: 用户点赞表对象
        """
        return LikeMapper.select_like_by_id(id)
    

    def insert_like(self, like: Like) -> int:
        """
        新增用户点赞表

        Args:
            like (like): 用户点赞表对象

        Returns:
            int: 插入的记录数
        """
        return LikeMapper.insert_like(like)

    
    def update_like(self, like: Like) -> int:
        """
        修改用户点赞表

        Args:
            like (like): 用户点赞表对象

        Returns:
            int: 更新的记录数
        """
        return LikeMapper.update_like(like)
    

    
    def delete_like_by_ids(self, ids: List[int]) -> int:
        """
        批量删除用户点赞表

        Args:
            ids (List[int]): ID列表

        Returns:
            int: 删除的记录数
        """
        return LikeMapper.delete_like_by_ids(ids)
    

    def import_like(self, like_list: List[Like], is_update: bool = False) -> str:
        """
        导入用户点赞表数据

        Args:
            like_list (List[like]): 用户点赞表列表
            is_update (bool): 是否更新已存在的数据

        Returns:
            str: 导入结果消息
        """
        if not like_list:
            raise ServiceException("导入用户点赞表数据不能为空")

        success_count = 0
        fail_count = 0
        success_msg = ""
        fail_msg = ""

        for like in like_list:
            try:
                display_value = like
                
                display_value = getattr(like, "id", display_value)
                existing = None
                if like.id is not None:
                    existing = LikeMapper.select_like_by_id(like.id)
                if existing:
                    if is_update:
                        result = LikeMapper.update_like(like)
                    else:
                        fail_count += 1
                        fail_msg += f"<br/> 第{fail_count}条数据，已存在：{display_value}"
                        continue
                else:
                    result = LikeMapper.insert_like(like)
                
                if result > 0:
                    success_count += 1
                    success_msg += f"<br/> 第{success_count}条数据，操作成功：{display_value}"
                else:
                    fail_count += 1
                    fail_msg += f"<br/> 第{fail_count}条数据，操作失败：{display_value}"
            except Exception as e:
                fail_count += 1
                fail_msg += f"<br/> 第{fail_count}条数据，导入失败，原因：{e.__class__.__name__}"
                LogUtil.logger.error(f"导入用户点赞表失败，原因：{e}")

        if fail_count > 0:
            if success_msg:
                fail_msg = f"导入成功{success_count}条，失败{fail_count}条。{success_msg}<br/>" + fail_msg
            else:
                fail_msg = f"导入成功{success_count}条，失败{fail_count}条。{fail_msg}"
            raise ServiceException(fail_msg)
        success_msg = f"恭喜您，数据已全部导入成功！共 {success_count} 条，数据如下：" + success_msg
        return success_msg