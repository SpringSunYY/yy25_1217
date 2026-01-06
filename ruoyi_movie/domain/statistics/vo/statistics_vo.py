from typing import List, Optional, TypeVar, Generic

from pydantic import BaseModel, Field

T = TypeVar('T', int, float)


class StatisticsVo(BaseModel, Generic[T]):
    """
    统计总数对象
    """
    value: T
    name: str


class PieBarStatisticsVo(BaseModel):
    """
    饼状图统计对象
    """
    name: str
    tooltipText: str
    values: List[StatisticsVo]
