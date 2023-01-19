from datetime import datetime
from typing import Optional

from pydantic import BaseModel, PositiveInt, NonNegativeInt


class DonationCreate(BaseModel):
    full_amount: PositiveInt
    comment: Optional[str]


class DonationMy(DonationCreate):
    id: int
    create_date: Optional[datetime]

    class Config:
        orm_mode = True


class DonationDB(DonationMy):
    user_id: Optional[int]
    invested_amount: Optional[NonNegativeInt]
    close_date: Optional[datetime]
    fully_invested: Optional[bool]
