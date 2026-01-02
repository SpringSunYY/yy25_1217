# -*- coding: utf-8 -*-
# @Author  : YY
# @FileName: like_po.py
# @Time    : 2025-12-21 18:49:53

from typing import Optional
from datetime import datetime

from sqlalchemy import BigInteger, Boolean, Date, DateTime, Float, Integer, JSON, LargeBinary, Numeric, String, Text, Time
from sqlalchemy.orm import Mapped, mapped_column

from ruoyi_admin.ext import db

class LikePo(db.Model):
    """
    用户点赞表PO对象
    """
    __tablename__ = 'tb_like'
    __table_args__ = {'comment': '用户点赞表'}
    id: Mapped[int] = mapped_column(
        'id',
        BigInteger,
        primary_key=True,
        autoincrement=True,
        nullable=False,
        comment='点赞编号'
    )
    user_id: Mapped[Optional[int]] = mapped_column(
        'user_id',
        BigInteger,
        nullable=False,
        comment='用户'
    )
    user_name: Mapped[Optional[str]] = mapped_column(
        'user_name',
        String(255),
        nullable=False,
        comment='用户名'
    )
    movie_id: Mapped[Optional[int]] = mapped_column(
        'movie_id',
        BigInteger,
        nullable=False,
        comment='电影ID'
    )
    movie_title: Mapped[Optional[str]] = mapped_column(
        'movie_title',
        String(255),
        nullable=True,
        comment='名称'
    )
    cover_url: Mapped[Optional[str]] = mapped_column(
        'cover_url',
        String(255),
        nullable=True,
        comment='封面'
    )
    genres: Mapped[Optional[str]] = mapped_column(
        'genres',
        String(255),
        nullable=True,
        comment='类型'
    )
    directors: Mapped[Optional[str]] = mapped_column(
        'directors',
        String(255),
        nullable=True,
        comment='导演'
    )
    country: Mapped[Optional[str]] = mapped_column(
        'country',
        String(255),
        nullable=True,
        comment='国家地区'
    )
    actors: Mapped[Optional[str]] = mapped_column(
        'actors',
        String(255),
        nullable=True,
        comment='主演'
    )
    score: Mapped[Optional[str]] = mapped_column(
        'score',
        Numeric(10, 0),
        nullable=False,
        comment='分数'
    )
    create_time: Mapped[Optional[datetime]] = mapped_column(
        'create_time',
        DateTime,
        nullable=False,
        comment='创建时间'
    )
