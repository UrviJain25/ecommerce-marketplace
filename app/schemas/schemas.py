from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr


# ─── Auth / User ─────────────────────────────────────────────────────────────

class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: Optional[str] = "user"  # user | seller | admin


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str


class UserOut(BaseModel):
    id: int
    name: str
    email: str
    role: str
    created_at: datetime

    class Config:
        from_attributes = True


# ─── Category ────────────────────────────────────────────────────────────────

class CategoryCreate(BaseModel):
    name: str
    parent_id: Optional[int] = None


class CategoryOut(BaseModel):
    id: int
    name: str
    parent_id: Optional[int]

    class Config:
        from_attributes = True


# ─── Product ─────────────────────────────────────────────────────────────────

class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    stock_qty: int
    category_id: Optional[int] = None


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock_qty: Optional[int] = None
    category_id: Optional[int] = None


class ProductOut(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: float
    stock_qty: int
    category_id: Optional[int]
    seller_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ─── Cart ────────────────────────────────────────────────────────────────────

class CartItemAdd(BaseModel):
    product_id: int
    quantity: int = 1


class CartItemUpdate(BaseModel):
    quantity: int


class CartItemOut(BaseModel):
    id: int
    product_id: int
    quantity: int
    product: ProductOut

    class Config:
        from_attributes = True


class CartOut(BaseModel):
    items: List[CartItemOut]
    total: float

# ─── Orders ─────────────────────────────────────────────────────────────

class OrderItemOut(BaseModel):
    product_id: int
    quantity: int
    price: float

    class Config:
        from_attributes = True


class OrderOut(BaseModel):
    id: int
    user_id: int
    total_amount: float
    created_at: datetime
    items: List[OrderItemOut] = []

    class Config:
        from_attributes = True


# ─── Invoice ────────────────────────────────────────────────────────────

class InvoiceOut(BaseModel):
    id: int
    order_id: int
    total_amount: float
    created_at: datetime

    class Config:
        from_attributes = True


# ─── Alerts ─────────────────────────────────────────────────────────────

class AlertOut(BaseModel):
    id: int
    product_id: int
    message: str
    created_at: datetime

    class Config:
        from_attributes = True
