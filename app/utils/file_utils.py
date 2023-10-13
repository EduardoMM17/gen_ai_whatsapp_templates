from fastapi import HTTPException, status
from zipfile import ZipFile
import pandas as pd
import io


def convert_excel_to_csv(excel_bytes: bytes) -> dict:
    excel_file = io.BytesIO(excel_bytes)
    df = pd.read_excel(excel_file)
    data_csv_dict_list = df.to_dict(orient="records")
    return data_csv_dict_list


def convert_excel_to_csv_string(excel_bytes: bytes) -> str:
    excel_file = io.BytesIO(excel_bytes)
    df = pd.read_excel(excel_file)
    csv_string = df.to_csv(index=False)
    return csv_string
