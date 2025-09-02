import numpy as np
import random
import pandas as pd
import os

folder_loc = "D:\\Projects\\Forecasting\\text_to_sql_working\\"


file_names_list = [
    "customers.csv",
    "campaigns.csv",
    "customer_reviews_complete.csv",
    "interactions.csv",
    "support_tickets.csv",
    "transactions.csv",
]

for file_name in file_names_list:
    # file_name = "customers.csv"
    _file = os.path.join(folder_loc, "data", file_name)
    files_rd = pd.read_csv(_file, sep=",")
    df_columns = files_rd.columns.to_list()

    txt_file = os.path.join(folder_loc, "data", "columns_format.txt")

    with open(txt_file, "a") as file:
        _fn_p = "\n" + "Dataset: " + file_name + "\n"
        _cls = "- Columns:" + "\n"
        file.write(_fn_p)
        file.write(_cls)

        for _curr_col in df_columns:
            _unq_values = files_rd[_curr_col].drop_duplicates().to_list()
            _unq_values_2 = random.sample(_unq_values, min(3, len(_unq_values)))
            _unq_values_2 = [v for v in _unq_values_2 if (v != "nan")]
            _unq_values_2 = [v for v in _unq_values_2 if not pd.isna(v)]
            if files_rd[_curr_col].dtypes == "object":
                _col_char = (
                    "    -"
                    + _curr_col
                    + "(type:character,sample values:"
                    + str(_unq_values_2)
                    + "),"
                    + "\n"
                )
                file.write(_col_char)

            elif files_rd[_curr_col].dtypes == "int64":
                _col_int = (
                    "    -"
                    + _curr_col
                    + "(type:integer,sample values:"
                    + str(_unq_values_2)
                    + "),"
                    + "\n"
                )
                file.write(_col_int)

            elif files_rd[_curr_col].dtypes == "float64":
                _col_float = (
                    "    -"
                    + _curr_col
                    + "(type:float,sample values:"
                    + str(_unq_values_2)
                    + "),"
                    + "\n"
                )
                file.write(_col_float)

            elif files_rd[_curr_col].dtypes == "bool":
                _col_bool = (
                    "    -"
                    + _curr_col
                    + "(type:bool,sample values:"
                    + str(_unq_values_2)
                    + "),"
                    + "\n"
                )
                file.write(_col_bool)
            else:
                print("Error")


print("Completed")
