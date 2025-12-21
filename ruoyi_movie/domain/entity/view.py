# -*- coding: utf-8 -*-
# @Author  : YY
# @FileName: view.py
# @Time    : 2025-12-21 18:49:52

from typing import Optional, Annotated
from datetime import datetime
from pydantic import Field, BeforeValidator
from ruoyi_common.base.model import BaseEntity
from ruoyi_common.base.transformer import to_datetime, str_to_int
from ruoyi_common.base.schema_excel import ExcelField
from ruoyi_common.base.schema_vo import VoField


class View(BaseEntity):
    """
    用户浏览表对象
    """
    # 浏览编号
    id: Annotated[
        Optional[int],
        BeforeValidator(str_to_int),
        Field(default=None, description="浏览编号"),
        VoField(query=True),
        ExcelField(name="浏览编号")
    ]
    # 用户
    user_id: Annotated[
        Optional[int],
        BeforeValidator(str_to_int),
        Field(default=None, description="用户"),
        ExcelField(name="用户")
    ]
    # 用户名
    user_name: Annotated[
        Optional[str],
        Field(default=None, description="用户名"),
        VoField(query=True),
        ExcelField(name="用户名")
    ]
    # 电影ID
    movie_id: Annotated[
        Optional[int],
        BeforeValidator(str_to_int),
        Field(default=None, description="电影ID"),
        ExcelField(name="电影ID")
    ]
    # 名称
    movie_title: Annotated[
        Optional[str],
        Field(default=None, description="名称"),
        VoField(query=True),
        ExcelField(name="名称")
    ]
    # 封面
    cover_url: Annotated[
        Optional[str],
        Field(default=None, description="封面"),
        ExcelField(name="封面")
    ]
    # 类型
    genres: Annotated[
        Optional[str],
        Field(default=None, description="类型"),
        VoField(query=True),
        ExcelField(name="类型")
    ]
    # 导演
    directors: Annotated[
        Optional[str],
        Field(default=None, description="导演"),
        VoField(query=True),
        ExcelField(name="导演")
    ]
    # 国家地区
    country: Annotated[
        Optional[str],
        Field(default=None, description="国家地区"),
        VoField(query=True),
        ExcelField(name="国家地区")
    ]
    # 主演
    actors: Annotated[
        Optional[str],
        Field(default=None, description="主演"),
        VoField(query=True),
        ExcelField(name="主演")
    ]
    # 分数
    score: Annotated[
        Optional[float],
        Field(default=None, description="分数"),
        ExcelField(name="分数")
    ]
    # 创建时间
    create_time: Annotated[
        Optional[datetime],
        BeforeValidator(to_datetime()),
        Field(default=None, description="创建时间"),
        VoField(query=True),
        ExcelField(name="创建时间")
    ]

    # 页码
    page_num: Optional[int] = Field(default=1, description="页码")
    # 每页数量
    page_size: Optional[int] = Field(default=10, description="每页数量")