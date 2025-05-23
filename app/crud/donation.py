from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Donation, User
from app.services.investment import invest


class CRUDDonation(CRUDBase):

    async def get_by_user(
            self,
            user: User,
            session: AsyncSession,
    ):
        reservations = await session.execute(
            select(Donation).where(
                Donation.user_id == user.id,
            )
        )
        return reservations.scalars().all()

    async def create_with_investment(
            self,
            obj_in,
            session: AsyncSession,
            user: User,
    ):
        obj_in_data = obj_in.dict()
        obj_in_data['user_id'] = user.id
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await invest(session)
        await session.refresh(db_obj)
        return db_obj


donation_crud = CRUDDonation(Donation)
