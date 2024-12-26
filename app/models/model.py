import datetime
from typing import TYPE_CHECKING, List, Optional
import uuid
from sqlalchemy import ForeignKey
from sqlmodel import Field, Relationship, SQLModel, INT, BOOLEAN, SMALLINT, NVARCHAR, NCHAR, DATETIME, FLOAT
# from app.models.productModel_model import ProductModel

# if TYPE_CHECKING:
#     from .productModel_model import ProductModel


class ProductModelBase(SQLModel, table=True):
    __tablename__ = 'ProductModel'
    __table_args__ = {"schema": "Production"}

    Name: str = Field(nullable=False, index=True)
    CatalogDescription: str | None = Field(default=None)
    Instructions: str | None = Field(default=None)
    rowguid: str = Field(default_factory=lambda: str(uuid.uuid4()), nullable=False, unique=True)
    ModifiedDate: Optional[datetime.datetime] = Field(default_factory=datetime.datetime.utcnow, sa_type=DATETIME, nullable=False)


class ProductModel(ProductModelBase, table=True):
    ProductModelID: int | None = Field(default=None, primary_key=True)
    products: List["Product"] = Relationship(back_populates="ProductModelInfo", sa_relationship=ForeignKey("Production.Product.ProductModelID"))


class ProductBase(SQLModel, table=True):
    __tablename__ = "Product"
    __table_args__ = {"schema": "Production"}

    Name: str = Field(sa_type=NVARCHAR(50), nullable=False)
    ProductNumber: str = Field(sa_type=NVARCHAR(25), nullable=False)
    SafetyStockLevel: int = Field(sa_type=SMALLINT, nullable=False)
    MakeFlag: bool = Field(default=True, sa_type=BOOLEAN, nullable=False)
    ReorderPoint: int = Field(sa_type=SMALLINT, nullable=False)
    StandardCost: float = Field(sa_type=FLOAT, nullable=False)
    ListPrice: float = Field(sa_type=FLOAT, nullable=False)
    DaysToManufacture: int = Field(sa_type=INT, nullable=False)
    SellStartDate: datetime.datetime = Field(sa_type=DATETIME, nullable=False)

    FinishedGoodsFlag: bool = Field(default=True, sa_type=BOOLEAN, nullable=False)
    Color: str | None = Field(default=None, sa_type=NVARCHAR(15))
    Size: str | None = Field(default=None, sa_type=NVARCHAR(5))
    SizeUnitMeasureCode: str | None = Field(default=None, sa_type=NCHAR(3))
    WeightUnitMeasureCode: str | None = Field(default=None, sa_type=NCHAR(3))
    Weight: float | None = Field(default=None, sa_type=FLOAT)
    ProductLine: str | None = Field(default=None, sa_type=NCHAR(2))
    Class: str | None = Field(default=None, sa_type=NCHAR(2))
    Style: str | None = Field(default=None, sa_type=NCHAR(2))
    ProductSubcategoryID: int | None = Field(default=None, sa_type=INT)

    ProductModelID: int | None = Field(default=None, foreign_key="Production.ProductModel.ProductModelID")
    ProductModelInfo: Optional["ProductModel"] = Relationship(back_populates="products", sa_relationship=ForeignKey("Production.ProductModel.ProductModelID"))

    SellEndDate: datetime.datetime | None = Field(default=None, sa_type=DATETIME)
    DiscontinuedDate: datetime.datetime | None = Field(default=None, sa_type=DATETIME)
    rowguid: str = Field(default_factory=lambda: str(uuid.uuid4()), sa_type=NVARCHAR(36), nullable=False)
    ModifiedDate: Optional[datetime.datetime] = Field(default_factory=datetime.datetime.utcnow, sa_type=DATETIME, nullable=False)


class Product(ProductBase, table=True):
    ProductID: int | None = Field(default=None, primary_key=True)


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    Name: str | None = None
    ProductNumber: str | None = None
    SafetyStockLevel: int | None = None
    MakeFlag: bool | None = None
    ReorderPoint: int | None = None
    StandardCost: float | None = None
    ListPrice: float | None = None
    DaysToManufacture: int | None = None
    SellStartDate: datetime.datetime | None = None
