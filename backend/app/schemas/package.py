from decimal import Decimal

from pydantic import BaseModel, Field


class PackageBase(BaseModel):
    title: str = Field(min_length=2, max_length=255)
    description: str = Field(min_length=5)
    price: Decimal = Field(ge=0, max_digits=10, decimal_places=2)
    included_services: str = Field(min_length=5)
    is_active: bool = True


class PackageCreate(PackageBase):
    pass


class PackageUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=2, max_length=255)
    description: str | None = Field(default=None, min_length=5)
    price: Decimal | None = Field(default=None, ge=0, max_digits=10, decimal_places=2)
    included_services: str | None = Field(default=None, min_length=5)
    is_active: bool | None = None


class PackageRead(PackageBase):
    id: int

    model_config = {"from_attributes": True}
