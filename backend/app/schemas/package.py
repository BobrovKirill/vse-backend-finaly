from decimal import Decimal

from pydantic import BaseModel, Field, HttpUrl


class ServiceBase(BaseModel):
    title: str = Field(min_length=2, max_length=255)
    description: str | None = None
    price: Decimal | None = Field(default=None, ge=0, max_digits=10, decimal_places=2)
    is_active: bool = True


class ServiceCreate(ServiceBase):
    pass


class ServiceUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=2, max_length=255)
    description: str | None = None
    price: Decimal | None = Field(default=None, ge=0, max_digits=10, decimal_places=2)
    is_active: bool | None = None


class ServiceRead(ServiceBase):
    id: int

    model_config = {"from_attributes": True}


class PackageServiceCreate(BaseModel):
    service_id: int
    position: int = Field(default=0, ge=0)


class PackageServiceRead(BaseModel):
    id: int
    position: int
    service: ServiceRead

    model_config = {"from_attributes": True}


class PackageBase(BaseModel):
    title: str = Field(min_length=2, max_length=255)
    description: str = Field(min_length=5)
    price: Decimal = Field(ge=0, max_digits=10, decimal_places=2)
    checkout_url: HttpUrl | None = None
    is_active: bool = True


class PackageCreate(PackageBase):
    pass


class PackageUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=2, max_length=255)
    description: str | None = Field(default=None, min_length=5)
    price: Decimal | None = Field(default=None, ge=0, max_digits=10, decimal_places=2)
    checkout_url: HttpUrl | None = None
    is_active: bool | None = None


class PackageRead(PackageBase):
    id: int
    services: list[PackageServiceRead] = []

    model_config = {"from_attributes": True}
