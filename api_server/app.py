from fastapi import FastAPI
from pydantic import BaseModel

from gpts.drug_searcher import exec_query

app = FastAPI()

# router = APIRouter()


@app.get("/health")
def read_root():
    return "OK"


class Query(BaseModel):
    query: str


@app.post("/query")
def query_df(query: Query):
    return exec_query(query.query)


# app.include_router(router)
