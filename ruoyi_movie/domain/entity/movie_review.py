# -*- coding: utf-8 -*-
# @Author  : YY
# @FileName: movie_review.py
# @Time    : 2025-12-21 18:49:52

from typing import Optional, Annotated
from datetime import datetime
from pydantic import Field, BeforeValidator
from ruoyi_common.base.model import BaseEntity
from ruoyi_common.base.transformer import to_datetime, str_to_int
from ruoyi_common.base.schema_excel import ExcelField
from ruoyi_common.base.schema_vo import VoField


class MovieReview(BaseEntity):
    """
    影评信息表对象
    """
    # 编号
    id: Annotated[
        Optional[int],
        BeforeValidator(str_to_int),
        Field(default=None, description="编号"),
        VoField(query=True),
        ExcelField(name="编号",action="export")
    ]
    # 评论ID
    review_id: Annotated[
        Optional[int],
        BeforeValidator(str_to_int),
        Field(default=None, description="评论ID"),
        VoField(query=True),
        ExcelField(name="评论ID")
    ]
    # 电影ID
    movie_id: Annotated[
        Optional[int],
        BeforeValidator(str_to_int),
        Field(default=None, description="电影ID"),
        VoField(query=True),
        ExcelField(name="电影ID")
    ]
    # 评论类型
    type: Annotated[
        Optional[str],
        Field(default=None, description="评论类型"),
        VoField(query=True),
        ExcelField(name="评论类型", dict_type="review_type")
    ]
    # 用户名
    user_name: Annotated[
        Optional[str],
        Field(default=None, description="用户名"),
        VoField(query=True),
        ExcelField(name="用户名")
    ]
    # 星级（1–5）
    rating_star: Annotated[
        Optional[int],
        BeforeValidator(str_to_int),
        Field(default=None, description="星级（1–5）"),
        VoField(query=True),
        ExcelField(name="星级")
    ]
    # 有用数
    votes_up: Annotated[
        Optional[int],
        BeforeValidator(str_to_int),
        Field(default=None, description="有用数"),
        ExcelField(name="有用数")
    ]
    # 没用数
    votes_down: Annotated[
        Optional[int],
        BeforeValidator(str_to_int),
        Field(default=None, description="没用数"),
        ExcelField(name="没用数")
    ]
    # 回应数
    replies_count: Annotated[
        Optional[int],
        BeforeValidator(str_to_int),
        Field(default=None, description="回应数"),
        ExcelField(name="回应数")
    ]
    # 时间
    comment_time: Annotated[
        Optional[datetime],
        BeforeValidator(to_datetime()),
        Field(default=None, description="时间"),
        VoField(query=True),
        ExcelField(name="时间")
    ]
    # 影评标题
    review_title: Annotated[
        Optional[str],
        Field(default=None, description="影评标题"),
        VoField(query=True),
        ExcelField(name="影评标题")
    ]
    # 用户头像
    user_avatar: Annotated[
        Optional[str],
        Field(default=None, description="用户头像"),
        ExcelField(name="用户头像")
    ]
    # 内容
    content: Annotated[
        Optional[str],
        Field(default=None, description="内容"),
        ExcelField(name="内容")
    ]

    # 页码
    page_num: Optional[int] = Field(default=1, description="页码")
    # 每页数量
    page_size: Optional[int] = Field(default=10, description="每页数量")
