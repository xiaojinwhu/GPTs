from fastapi import APIRouter, FastAPI
from pydantic import BaseModel

from gpts.drug_searcher import exec_query

app = FastAPI()

router = APIRouter()


class Query(BaseModel):
    query: str


@router.post("/query")
def query_df(query: Query):
    return exec_query(query.query)


app.include_router(router)
