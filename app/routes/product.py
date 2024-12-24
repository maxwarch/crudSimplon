from typing import Annotated, List, Tuple

from bson.json_util import loads
from fastapi import APIRouter, Query, Request, Response
from app.enums import AlertType
from app.types import ParamsForFetchDb
from app.helpers.json_parser import JSONEncoder
from app.helpers.fetch_db import data_to_manipulate, fetch_helper
from solsius.utils.medical_alert import detect_all_delta
from solsius.utils.manipulate import Manipulate


router = APIRouter(
    prefix="/alerts",
    tags=["alerts"],
    responses={404: {"description": "Not found"}},
)

class DataToCompute(ParamsForFetchDb):
    threshold_temperature: Annotated[float, Query(title='Threshold temp', default=2.2, gt=0)]
    time_delta: Annotated[str, Query(title='Timedelta', default='48h')]



@router.post("/medical")
def medical(params: DataToCompute):
    mans = data_to_manipulate(params.user, params.soles, params.records)

    result = medical_check_deltas(mans, params.time_delta, float(params.threshold_temperature))

    return Response(JSONEncoder().encode((AlertType.temperature.value, result)), media_type = "application/json")


@router.post("/medical/fetch")
async def medical_fetch(request: Request, params: DataToCompute):
    mans = await fetch_helper(request.app.db, params.user, params.start_time)
    result = None

    if mans is not None:
        result = medical_check_deltas(mans, params.time_delta, float(params.threshold_temperature))

    return Response(JSONEncoder().encode((AlertType.temperature.value, result)), media_type="application/json")




def medical_check_deltas(mans: List[Tuple[str, Manipulate]], time_delta: str, threshold_temperature: float):
    results: List[str] = []
    
    for sole_id, man in mans:

        if man.data.shape[0] > 0:
            deltas = detect_all_delta(man.data, threshold_temperature=threshold_temperature, time_delta=time_delta)
            
            for index, delta in enumerate(deltas):
                if delta is not None and len(delta[1]) > 0:
                    deltas[index] = loads(delta[1].to_json(orient='records'))[0]
            
            if (all(item is None for item in deltas)) is False:
                results.append(
                    dict(
                        threshold = threshold_temperature, 
                        solesId = sole_id,
                        deltas = deltas
                    )
                )

    return results