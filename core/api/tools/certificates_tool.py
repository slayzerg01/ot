from fastapi import HTTPException
from sqlalchemy import and_, select, or_, delete, update
from sqlalchemy.orm import joinedload
from core.models.exam import Certificate
from sqlalchemy.engine import Result
from core.api.schemas.certificate import CertificateResponse
from sqlalchemy.ext.asyncio import AsyncSession


async def get_all_certificates(session: AsyncSession) -> list[CertificateResponse]:
    stmt = select(Certificate).options(joinedload(Certificate.employee)).order_by(Certificate.number)
    res: Result = await session.execute(stmt)
    certificates: list[Certificate] = res.scalars().all()
    result = []
    for item in certificates:
        
        certificate : Certificate = item
        res: CertificateResponse = CertificateResponse(
            number=certificate.number,
            employee= certificate.employee.FIO if certificate.employee else None
        )
        result.append(res)
    return result