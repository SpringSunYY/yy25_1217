from typing import Optional, Annotated

from pydantic import Field, BeforeValidator

from ruoyi_common.base.model import BaseEntity
from ruoyi_common.base.schema_vo import VoField
from ruoyi_common.base.transformer import str_to_int


class MovieStatisticsRequest(BaseEntity):
    # 开始时间
    start_time: Annotated[
        Optional[str],
        Field(default=None, description="开始时间"),
        VoField(query=True),
    ]
    # 结束时间
    end_time: Annotated[
        Optional[str],
        Field(default=None, description="结束时间"),
        VoField(query=True),
    ]
    # 数量
    count_number: Annotated[
        Optional[int],
        BeforeValidator(str_to_int),
        Field(default=100, ge=1, le=1000, description="数量"),
        VoField(query=True),
    ]
    # 类型
    genres: Annotated[
        Optional[str],
        Field(default=None, description="类型"),
        VoField(query=True),
    ]
