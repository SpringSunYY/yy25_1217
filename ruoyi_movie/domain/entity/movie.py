# -*- coding: utf-8 -*-
# @Author  : YY
# @FileName: movie.py
# @Time    : 2025-12-21 18:49:53

from typing import Optional, Annotated
from datetime import datetime
from pydantic import Field, BeforeValidator
from ruoyi_common.base.model import BaseEntity
from ruoyi_common.base.transformer import to_datetime, str_to_int
from ruoyi_common.base.schema_excel import ExcelField
from ruoyi_common.base.schema_vo import VoField


class Movie(BaseEntity):
    """
    电影信息表对象
    """
    # 编号
    id: Annotated[
        Optional[int],
        BeforeValidator(str_to_int),
        Field(default=None, description="编号"),
        VoField(query=True),
        ExcelField(name="编号")
    ]
    # 电影ID
    movie_id: Annotated[
        Optional[int],
        BeforeValidator(str_to_int),
        Field(default=None, description="电影ID"),
        VoField(query=True),
        ExcelField(name="电影ID")
    ]
    # 名称
    title: Annotated[
        Optional[str],
        Field(default=None, description="名称"),
        VoField(query=True),
        ExcelField(name="名称")
    ]
    # 评分
    rating: Annotated[
        Optional[float],
        Field(default=None, description="评分"),
        VoField(query=True),
        ExcelField(name="评分")
    ]
    # 看过人数
    view_count: Annotated[
        Optional[int],
        BeforeValidator(str_to_int),
        Field(default=None, description="看过人数"),
        ExcelField(name="看过人数")
    ]
    # 想看人数
    wish_count: Annotated[
        Optional[int],
        BeforeValidator(str_to_int),
        Field(default=None, description="想看人数"),
        ExcelField(name="想看人数")
    ]
    # 总影评数
    reviews_count: Annotated[
        Optional[int],
        BeforeValidator(str_to_int),
        Field(default=None, description="总影评数"),
        ExcelField(name="总影评数")
    ]
    # 语言
    language: Annotated[
        Optional[str],
        Field(default=None, description="语言"),
        VoField(query=True),
        ExcelField(name="语言")
    ]
    # 国家地区
    country: Annotated[
        Optional[str],
        Field(default=None, description="国家地区"),
        VoField(query=True),
        ExcelField(name="国家地区")
    ]
    # 导演
    directors: Annotated[
        Optional[str],
        Field(default=None, description="导演"),
        VoField(query=True),
        ExcelField(name="导演")
    ]
    # 编剧
    writers: Annotated[
        Optional[str],
        Field(default=None, description="编剧"),
        VoField(query=True),
        ExcelField(name="编剧")
    ]
    # 主演
    actors: Annotated[
        Optional[str],
        Field(default=None, description="主演"),
        VoField(query=True),
        ExcelField(name="主演")
    ]
    # 片长
    duration: Annotated[
        Optional[str],
        Field(default=None, description="片长"),
        ExcelField(name="片长")
    ]
    # 片长（分钟）
    duration_minute: Annotated[
        Optional[int],
        BeforeValidator(str_to_int),
        Field(default=None, description="片长（分钟）"),
        ExcelField(name="片长（分钟）")
    ]
    # 上映日期
    pub_date: Annotated[
        Optional[str],
        Field(default=None, description="上映日期"),
        ExcelField(name="上映日期")
    ]
    # 上映时间
    publish_date: Annotated[
        Optional[datetime],
        BeforeValidator(to_datetime()),
        Field(default=None, description="上映时间"),
        VoField(query=True),
        ExcelField(name="上映时间")
    ]
    # 上映年份
    publish_year: Annotated[
        Optional[int],
        BeforeValidator(str_to_int),
        Field(default=None, description="上映年份"),
        VoField(query=True),
        ExcelField(name="上映年份")
    ]
    # 类型
    genres: Annotated[
        Optional[str],
        Field(default=None, description="类型"),
        VoField(query=True),
        ExcelField(name="类型")
    ]
    # 剧情简介
    summary: Annotated[
        Optional[str],
        Field(default=None, description="剧情简介"),
        ExcelField(name="剧情简介")
    ]
    # 封面
    cover_url: Annotated[
        Optional[str],
        Field(default=None, description="封面"),
        ExcelField(name="封面")
    ]
    # 详情页
    detail_url: Annotated[
        Optional[str],
        Field(default=None, description="详情页"),
        ExcelField(name="详情页")
    ]

    # 页码
    page_num: Optional[int] = Field(default=1, description="页码")
    # 每页数量
    page_size: Optional[int] = Field(default=10, description="每页数量")