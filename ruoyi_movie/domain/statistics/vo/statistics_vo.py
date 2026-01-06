from typing import List, Optional

from pydantic import BaseModel, Field


class StatisticsVo(BaseModel):
    """
    统计总数对象
    """
    value: int
    name: str


class PieBarStatisticsVo(BaseModel):
    """
    饼状图统计对象
    """
    name: str
    tooltipText: str
    values: List[StatisticsVo]




