from pydantic import BaseModel, Field


class HealthIndicatorBase(BaseModel):
    code: str = Field(min_length=2, max_length=100)
    title: str = Field(min_length=2, max_length=255)
    description: str | None = None
    is_active: bool = True


class HealthIndicatorCreate(HealthIndicatorBase):
    pass


class HealthIndicatorUpdate(BaseModel):
    code: str | None = Field(default=None, min_length=2, max_length=100)
    title: str | None = Field(default=None, min_length=2, max_length=255)
    description: str | None = None
    is_active: bool | None = None


class HealthIndicatorRead(HealthIndicatorBase):
    id: int

    model_config = {"from_attributes": True}


class PackageRuleBase(BaseModel):
    indicator_id: int
    min_score: int = Field(default=0, ge=0)
    max_score: int | None = Field(default=None, ge=0)
    weight: int = Field(default=1, ge=1)


class PackageRuleCreate(PackageRuleBase):
    pass


class PackageRuleUpdate(BaseModel):
    indicator_id: int | None = None
    min_score: int | None = Field(default=None, ge=0)
    max_score: int | None = Field(default=None, ge=0)
    weight: int | None = Field(default=None, ge=1)


class PackageRuleRead(PackageRuleBase):
    id: int
    package_id: int

    model_config = {"from_attributes": True}
