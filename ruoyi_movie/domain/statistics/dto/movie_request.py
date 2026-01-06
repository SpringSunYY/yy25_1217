from typing import Optional, Annotated, List

from pydantic import Field

from ruoyi_common.base.model import BaseEntity
from ruoyi_common.base.schema_excel import ExcelField
from ruoyi_common.base.schema_vo import VoField


class MovieStatisticsRequest(BaseEntity):
    # 开始时间
    start_time: Annotated[
        Optional[str],
        Field(default=None, description="开始时间"),
        VoField(query=True),
        ExcelField(name="开始时间")
    ]
    # 结束时间
    end_time: Annotated[
        Optional[str],
        Field(default=None, description="结束时间"),
        VoField(query=True),
        ExcelField(name="结束时间")
    ]

