# backend/app/schemas/__init__.py
from . import category, product, user, order, order_item

category.Category.model_rebuild()
product.Product.model_rebuild()
user.User.model_rebuild()
order.Order.model_rebuild()
order_item.OrderItem.model_rebuild()