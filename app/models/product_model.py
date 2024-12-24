import datetime
from typing import Optional
import uuid
from sqlmodel import Field, SQLModel, Column, INT, BOOLEAN, DECIMAL, SMALLINT, NVARCHAR, NCHAR, DATETIME, FLOAT


class ProductBase(SQLModel):
    __tablename__ = "Product"
    __table_args__ = {"schema": "Production"}

    Name: str = Field(sa_column=Column(NVARCHAR(50), nullable=False))
    ProductNumber: str = Field(sa_column=Column(NVARCHAR(25), nullable=False))
    SafetyStockLevel: int = Field(sa_column=Column(SMALLINT, nullable=False))
    MakeFlag: bool = Field(default=True, sa_column=Column(BOOLEAN, nullable=False))
    ReorderPoint: int = Field(sa_column=Column(SMALLINT, nullable=False))
    StandardCost: float = Field(sa_column=Column(FLOAT, nullable=False))
    ListPrice: float = Field(sa_column=Column(FLOAT, nullable=False))
    DaysToManufacture: int = Field(sa_column=Column(INT, nullable=False))
    SellStartDate: datetime.datetime = Field(sa_column=Column(DATETIME, nullable=False))
    FinishedGoodsFlag: bool = Field(default=True, sa_column=Column(BOOLEAN, nullable=False))
    Color: str | None = Field(default=None, sa_column=Column(NVARCHAR(15)))
    Size: str | None = Field(default=None, sa_column=Column(NVARCHAR(5)))
    SizeUnitMeasureCode: str | None = Field(default=None, sa_column=Column(NCHAR(3)))
    WeightUnitMeasureCode: str | None = Field(default=None, sa_column=Column(NCHAR(3)))
    Weight: float | None = Field(default=None, sa_column=Column(DECIMAL(5, 8)))
    ProductLine: str | None = Field(default=None, sa_column=Column(NCHAR(2)))
    Class: str | None = Field(default=None, sa_column=Column(NCHAR(2)))
    Style: str | None = Field(default=None, sa_column=Column(NCHAR(2)))
    ProductSubcategoryID: int | None = Field(default=None, sa_column=Column(INT))
    ProductModelID: int | None = Field(default=None, sa_column=Column(INT))
    SellEndDate: datetime.datetime | None = Field(default=None, sa_column=Column(DATETIME))
    DiscontinuedDate: datetime.datetime | None = Field(default=None, sa_column=Column(DATETIME))
    rowguid: str = Field(default_factory=lambda: str(uuid.uuid4()), sa_column=Column(NVARCHAR(36), nullable=False))
    ModifiedDate: Optional[datetime.datetime] = Field(default_factory=datetime.datetime.utcnow, sa_column=Column(DATETIME, nullable=False))


class Product(ProductBase, table=True):
    ProductID: int | None = Field(default=None, primary_key=True)


class ProductCreate(ProductBase):
    pass
