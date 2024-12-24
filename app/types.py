from typing import Annotated
from fastapi import Query
from pydantic import BaseModel


class ParamsForFetchDb(BaseModel):
    user: Annotated[str, Query(title='The user')]
    records: Annotated[str | list, Query(title='The records', default='')]
    soles: Annotated[str | list, Query(title='The soles', default=[])]
    start_time: Annotated[int, Query(title='start time', default=None)]

class ParamsToManipulate(ParamsForFetchDb):
    soles: Annotated[str | list, Query(title='The soles')]
