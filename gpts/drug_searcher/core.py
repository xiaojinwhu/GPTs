import os

import pandas as pd
from pandasql import sqldf
from rich import print

DATA_PATH = os.getenv("DATA_PATH") or "data/drugs.csv"

drug_df = pd.read_csv(
    DATA_PATH,
)

print(drug_df.head(5))

globals_dict = {
    "drug_df": drug_df,
}
locals_dict = {}


def exec_query(sql):
    # # result = ""
    # exec(exec_string, globals_dict, locals_dict)

    # result = locals_dict["result"].to_markdown()

    result = sqldf(sql)
    return {"data": result}
