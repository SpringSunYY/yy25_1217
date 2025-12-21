# -*- coding: utf-8 -*-
# @Author  : YY
# @FileName: movie_review_po.py
# @Time    : 2025-12-21 18:49:52

from typing import Optional
from datetime import datetime

from sqlalchemy import BigInteger, Boolean, Date, DateTime, Float, Integer, JSON, LargeBinary, Numeric, String, Text, Time
from sqlalchemy.orm import Mapped, mapped_column

from ruoyi_admin.ext import db

class MovieReviewPo(db.Model):
    """
    影评信息表PO对象
    """
    __tablename__ = 'tb_movie_review'
    __table_args__ = {'comment': '影评信息表'}
    id: Mapped[Optional[int]] = mapped_column(
        'id',
        BigInteger,
        nullable=False,
        comment='编号'
    )
    review_id: Mapped[int] = mapped_column(
        'review_id',
        BigInteger,
        primary_key=True,
        autoincrement=False,
        nullable=False,
        comment='评论ID'
    )
    movie_id: Mapped[Optional[int]] = mapped_column(
        'movie_id',
        BigInteger,
        nullable=False,
        comment='电影ID'
    )
    type: Mapped[Optional[str]] = mapped_column(
        'type',
        String(255),
        nullable=True,
        comment='评论类型'
    )
    user_name: Mapped[Optional[str]] = mapped_column(
        'user_name',
        String(255),
        nullable=True,
        comment='用户名'
    )
    rating_star: Mapped[Optional[int]] = mapped_column(
        'rating_star',
        Integer,
        nullable=True,
        comment='星级（1–5）'
    )
    votes_up: Mapped[Optional[int]] = mapped_column(
        'votes_up',
        Integer,
        nullable=True,
        comment='有用数'
    )
    votes_down: Mapped[Optional[int]] = mapped_column(
        'votes_down',
        Integer,
        nullable=True,
        comment='没用数'
    )
    replies_count: Mapped[Optional[int]] = mapped_column(
        'replies_count',
        Integer,
        nullable=True,
        comment='回应数'
    )
    comment_time: Mapped[Optional[datetime]] = mapped_column(
        'comment_time',
        DateTime,
        nullable=True,
        comment='时间'
    )
    review_title: Mapped[Optional[str]] = mapped_column(
        'review_title',
        String(255),
        nullable=True,
        comment='影评标题'
    )
    user_avatar: Mapped[Optional[str]] = mapped_column(
        'user_avatar',
        String(255),
        nullable=True,
        comment='用户头像'
    )
    content: Mapped[Optional[str]] = mapped_column(
        'content',
        Text,
        nullable=True,
        comment='内容'
    )