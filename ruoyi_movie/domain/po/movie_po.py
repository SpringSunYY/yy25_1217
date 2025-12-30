# -*- coding: utf-8 -*-
# @Author  : YY
# @FileName: movie_po.py
# @Time    : 2025-12-21 18:49:53

from typing import Optional
from datetime import datetime

from sqlalchemy import BigInteger, Boolean, Date, DateTime, Float, Integer, JSON, LargeBinary, Numeric, String, Text, Time
from sqlalchemy.orm import Mapped, mapped_column

from ruoyi_admin.ext import db

class MoviePo(db.Model):
    """
    电影信息表PO对象
    """
    __tablename__ = 'tb_movie'
    __table_args__ = {'comment': '电影信息表'}
    id: Mapped[int] = mapped_column(
        'id',
        BigInteger,
        primary_key=True,
        autoincrement=True,
        nullable=False,
        comment='编号'
    )
    movie_id: Mapped[Optional[int]] = mapped_column(
        'movie_id',
        BigInteger,
        nullable=False,
        comment='电影ID'
    )
    title: Mapped[Optional[str]] = mapped_column(
        'title',
        String(255),
        nullable=False,
        comment='名称'
    )
    rating: Mapped[Optional[str]] = mapped_column(
        'rating',
        Numeric(10, 0),
        nullable=True,
        comment='评分'
    )
    view_count: Mapped[Optional[int]] = mapped_column(
        'view_count',
        Integer,
        nullable=True,
        comment='看过人数'
    )
    wish_count: Mapped[Optional[int]] = mapped_column(
        'wish_count',
        Integer,
        nullable=True,
        comment='想看人数'
    )
    reviews_count: Mapped[Optional[int]] = mapped_column(
        'reviews_count',
        Integer,
        nullable=True,
        comment='总影评数'
    )
    language: Mapped[Optional[str]] = mapped_column(
        'language',
        String(255),
        nullable=True,
        comment='语言'
    )
    country: Mapped[Optional[str]] = mapped_column(
        'country',
        String(255),
        nullable=True,
        comment='国家地区'
    )
    directors: Mapped[Optional[str]] = mapped_column(
        'directors',
        String(255),
        nullable=True,
        comment='导演'
    )
    writers: Mapped[Optional[str]] = mapped_column(
        'writers',
        String(255),
        nullable=True,
        comment='编剧'
    )
    actors: Mapped[Optional[str]] = mapped_column(
        'actors',
        String(255),
        nullable=True,
        comment='主演'
    )
    duration: Mapped[Optional[str]] = mapped_column(
        'duration',
        String(255),
        nullable=True,
        comment='片长'
    )
    duration_minute: Mapped[Optional[int]] = mapped_column(
        'duration_minute',
        Integer,
        nullable=True,
        comment='片长（分钟）'
    )
    pub_date: Mapped[Optional[str]] = mapped_column(
        'pub_date',
        String(255),
        nullable=True,
        comment='上映日期'
    )
    publish_date: Mapped[Optional[datetime]] = mapped_column(
        'publish_date',
        DateTime,
        nullable=True,
        comment='上映时间'
    )
    publish_year: Mapped[Optional[int]] = mapped_column(
        'publish_year',
        Integer,
        nullable=True,
        comment='上映年份'
    )
    genres: Mapped[Optional[str]] = mapped_column(
        'genres',
        String(255),
        nullable=True,
        comment='类型'
    )
    summary: Mapped[Optional[str]] = mapped_column(
        'summary',
        Text,
        nullable=True,
        comment='剧情简介'
    )
    cover_url: Mapped[Optional[str]] = mapped_column(
        'cover_url',
        String(255),
        nullable=True,
        comment='封面'
    )
    detail_url: Mapped[Optional[str]] = mapped_column(
        'detail_url',
        String(255),
        nullable=True,
        comment='详情页'
    )