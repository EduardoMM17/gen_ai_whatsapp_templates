from fastapi import HTTPException, status
from zipfile import ZipFile
import pandas as pd
import io

from app.utils.file_utils import convert_excel_to_csv, convert_excel_to_csv_string


def process_zip_file(zip_bytes: bytes):
    db_in = False
    ticket_ids_from_db = []
    ticket_ids_from_files = []
    tickets_info = []
    raw_conversations = []
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
                            tickets_info.append(
                                {
                                    "ticketId": csv_dict["ticketId"],
                                    "name": csv_dict["name"],
                                    "contactReason": csv_dict["contactReason"],
                                    "npsScore": csv_dict["nps"],
                                }
                            )
                    else:
                        ticket_id = filename.split(".")[0]
                        ticket_ids_from_files.append(int(ticket_id))
                        raw_conversations.append(
                            {
                                "ticketId": int(ticket_id),
                                "content": convert_excel_to_csv_string(excel_bytes),
                            }
                        )

    if not db_in:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="bd.xlsx file not found"
        )
    for raw_conversation in raw_conversations:
        ticket_in = False
        for ticket in tickets_info:
            if ticket["ticketId"] == raw_conversation["ticketId"]:
                ticket_in = True
        if not ticket_in:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ticketIds from db do not match ticketIds from files",
            )

    return raw_conversations, tickets_info
