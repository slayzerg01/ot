from pydantic import BaseModel, ConfigDict


class CertificateBase(BaseModel):
    number: int
    model_config = ConfigDict(from_attributes=True)


class CertificateResponse(CertificateBase):
    employee: str | None
