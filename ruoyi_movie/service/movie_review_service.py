# -*- coding: utf-8 -*-
# @Author  : YY
# @FileName: movie_review_service.py
# @Time    : 2025-12-21 18:49:52

from typing import List

from ruoyi_common.exception import ServiceException
from ruoyi_common.utils.base import LogUtil
from ruoyi_movie.domain.entity import MovieReview
from ruoyi_movie.mapper.movie_review_mapper import MovieReviewMapper

class MovieReviewService:
    """影评信息表服务类"""

    def select_movie_review_list(self, movie_review: MovieReview) -> List[MovieReview]:
        """
        查询影评信息表列表

        Args:
            movie_review (movie_review): 影评信息表对象

        Returns:
            List[movie_review]: 影评信息表列表
        """
        return MovieReviewMapper.select_movie_review_list(movie_review)

    def select_movie_review_by_id(self, id: int) -> MovieReview:
        """
        根据ID查询影评信息表

        Args:
            id (int): 编号

        Returns:
            movie_review: 影评信息表对象
        """
        return MovieReviewMapper.select_movie_review_by_id(id)


    def insert_movie_review(self, movie_review: MovieReview) -> int:
        """
        新增影评信息表

        Args:
            movie_review (movie_review): 影评信息表对象

        Returns:
            int: 插入的记录数
        """
        # 首先查询是否已存在
        existing = MovieReviewMapper.select_movie_review_by_review_id(movie_review.review_id)
        if existing:
            raise ServiceException("已存在该影评")
        if existing.id != movie_review.id:
            raise ServiceException("该评论编号已存在，不可修改为此编号")
        return MovieReviewMapper.insert_movie_review(movie_review)

    def update_movie_review(self, movie_review: MovieReview) -> int:
        """
        修改影评信息表

        Args:
            movie_review (movie_review): 影评信息表对象

        Returns:
            int: 更新的记录数
        """
        existing = MovieReviewMapper.select_movie_review_by_review_id(movie_review.review_id)
        if not existing:
            raise ServiceException("不存在该影评")
        if existing.id != movie_review.id:
            raise ServiceException("该评论编号已存在，不可修改为此编号")
        return MovieReviewMapper.update_movie_review(movie_review)

    def delete_movie_review_by_ids(self, ids: List[int]) -> int:
        """
        批量删除影评信息表

        Args:
            ids (List[int]): ID列表

        Returns:
            int: 删除的记录数
        """
        return MovieReviewMapper.delete_movie_review_by_ids(ids)

    def import_movie_review(self, movie_review_list: List[MovieReview], is_update: bool = False) -> str:
        """
        导入影评信息表数据

        Args:
            movie_review_list (List[movie_review]): 影评信息表列表
            is_update (bool): 是否更新已存在的数据

        Returns:
            str: 导入结果消息
        """
        if not movie_review_list:
            raise ServiceException("导入影评信息表数据不能为空")

        success_count = 0
        fail_count = 0
        success_msg = ""
        fail_msg = ""

        for movie_review in movie_review_list:
            try:
                display_value = movie_review

                display_value = getattr(movie_review, "review_id", display_value)
                existing = None
                if movie_review.review_id is not None:
                    existing = MovieReviewMapper.select_movie_review_by_review_id(movie_review.review_id)
                if existing:
                    if is_update:
                        result = MovieReviewMapper.update_movie_review(movie_review)
                    else:
                        fail_count += 1
                        fail_msg += f"<br/> 第{fail_count}条数据，已存在：{display_value}"
                        continue
                else:
                    result = MovieReviewMapper.insert_movie_review(movie_review)

                if result > 0:
                    success_count += 1
                    success_msg += f"<br/> 第{success_count}条数据，操作成功：{display_value}"
                else:
                    fail_count += 1
                    fail_msg += f"<br/> 第{fail_count}条数据，操作失败：{display_value}"
            except Exception as e:
                fail_count += 1
                fail_msg += f"<br/> 第{fail_count}条数据，导入失败，原因：{e.__class__.__name__}"
                LogUtil.logger.error(f"导入影评信息表失败，原因：{e}")

        if fail_count > 0:
            if success_msg:
                fail_msg = f"导入成功{success_count}条，失败{fail_count}条。{success_msg}<br/>" + fail_msg
            else:
                fail_msg = f"导入成功{success_count}条，失败{fail_count}条。{fail_msg}"
            raise ServiceException(fail_msg)
        success_msg = f"恭喜您，数据已全部导入成功！共 {success_count} 条，数据如下：" + success_msg
        return success_msg
