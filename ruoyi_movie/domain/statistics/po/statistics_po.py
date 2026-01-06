from pydantic import BaseModel

class StatisticsPo(BaseModel):
    """
    统计总数对象
    """
    value: int
    name: str

