from fastapi import HTTPException, status
from zipfile import ZipFile
import pandas as pd
import io


def convert_excel_to_csv(excel_bytes: bytes) -> str:
    excel_file = io.BytesIO(excel_bytes)
    df = pd.read_excel(excel_file)
    data_csv_dict_list = df.to_dict(orient="records")
    return data_csv_dict_list


def process_zip_file(zip_bytes: bytes):
    db_in = False
    ticket_ids_from_db = []
    ticket_ids_from_files = []
    with ZipFile(io.BytesIO(zip_bytes)) as z:
        for filename in z.namelist():
            if filename.endswith((".xls", ".xlsx")):
                with z.open(filename) as f:
                    excel_bytes = f.read()
                    data_csv_dict_list = convert_excel_to_csv(excel_bytes)
                    if filename == "bd.xlsx":
                        db_in = True
                        for csv_dict in data_csv_dict_list:
                            ticket_ids_from_db.append(csv_dict["ticketId"])
                    else:
                        ticket_id = filename.split(".")[0]
                        ticket_ids_from_files.append(int(ticket_id))

    print(ticket_ids_from_db)
    print(ticket_ids_from_files)

    if not db_in:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="bd.xlsx file not found"
        )
    if sorted(ticket_ids_from_db) != sorted(ticket_ids_from_files):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ticketIds from db do not match ticketIds from files",
        )
