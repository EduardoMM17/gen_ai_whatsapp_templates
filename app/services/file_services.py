from fastapi import HTTPException, status
from zipfile import ZipFile
import pandas as pd
import io

from app.utils.file_utils import convert_excel_to_csv, convert_excel_to_csv_string


def process_zip_file(zip_bytes: bytes):
    with ZipFile(io.BytesIO(zip_bytes)) as z:
        file_data = extract_file_data(z)
    validate_file_data(file_data)
    return file_data["tickets_info"]


def extract_file_data(z):
    file_data = {"db_in": False, "tickets_info": [], "raw_conversations": []}
    for filename in z.namelist():
        if filename.endswith((".xls", ".xlsx")):
            with z.open(filename) as f:
                excel_bytes = f.read()
                data_csv_dict_list = convert_excel_to_csv(excel_bytes)
                process_excel_file(filename, excel_bytes, data_csv_dict_list, file_data)
    return file_data


def process_excel_file(filename, excel_bytes, data_csv_dict_list, file_data):
    if filename == "bd.xlsx":
        file_data["db_in"] = True
        for csv_dict in data_csv_dict_list:
            file_data["tickets_info"].append(
                {
                    "ticketId": csv_dict["ticketId"],
                    "name": csv_dict["name"],
                    "contactReason": csv_dict["contactReason"],
                    "npsScore": csv_dict["nps"],
                }
            )
    else:
        ticket_id = filename.split(".")[0]
        file_data["raw_conversations"].append(
            {"ticketId": ticket_id, "content": convert_excel_to_csv_string(excel_bytes)}
        )


def validate_file_data(file_data):
    if not file_data["db_in"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="bd.xlsx file not found"
        )
    for raw_conversation in file_data["raw_conversations"]:
        ticket_in = False
        for ticket in file_data["tickets_info"]:
            if int(ticket["ticketId"]) == int(raw_conversation["ticketId"]):
                ticket.update({"rawConversation": raw_conversation["content"]})
                ticket_in = True
        if not ticket_in:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ticketIds from db do not match ticketIds from files",
            )
