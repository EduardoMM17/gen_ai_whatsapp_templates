from pydantic import BaseModel


class BatchBase(BaseModel):
    processed: bool = False


class BatchCreate(BatchBase):
    company: str | None = None


class BatchInDBBase(BatchBase):
    id: int | None = None
    company_id: int | None = None
    submitter_id: int | None = None

    class Config:
        from_attributes = True


class Batch(BatchInDBBase):
    pass
