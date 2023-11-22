import os
from contextlib import asynccontextmanager

import databases
from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, Field

# 数据库配置
DATA_PATH = os.getenv("DATA_PATH", "data/drugs.db")
DATABASE_URL = f"sqlite:///{DATA_PATH}"
database = databases.Database(DATABASE_URL)


# # 在启动时连接数据库，在关闭时断开连接
# @app.on_event("startup")
# async def startup():
#     await database.connect()

# @app.on_event("shutdown")
# async def shutdown():
#     await database.disconnect()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()


# 创建FastAPI应用
app = FastAPI(
    lifespan=lifespan,
    title="药品知识库接口文档",
    description="药品知识库API",
    version="0.0.1",
    servers=[{"url": "https://yourdomain.here"}],
)


# 请求模型，仅接受SELECT语句
class SQLQuery(BaseModel):
    query: str = Field(..., description="SQL query to execute")
    model_config = {
        "json_schema_extra": {
            "examples": [{"query": "SELECT * FROM drug_info LIMIT 10"}]
        }
    }


# 依赖项，确保只执行SELECT语句
def validate_select_query(query: SQLQuery):
    if not query.query.strip().lower().startswith("select"):
        raise HTTPException(status_code=400, detail="Only SELECT queries are allowed.")
    return query


# 创建API路由
@app.post("/execute/", summary="Execute SQL query", operation_id="execute_sql")
async def execute(query: SQLQuery = Depends(validate_select_query)):
    try:
        # 使用参数化查询执行SQL语句
        result = await database.fetch_all(query=query.query)
        return {"result": result}
    except Exception as e:
        # 如果出现错误，返回错误信息
        raise HTTPException(status_code=400, detail=str(e))
