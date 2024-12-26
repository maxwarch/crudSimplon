import datetime
from typing import TYPE_CHECKING, List, Optional
import uuid
from sqlalchemy import DATETIME, Column, ForeignKey
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .product_model import Product


class ProductModelBase(SQLModel):
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
