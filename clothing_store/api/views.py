from django.shortcuts import render
from rest_framework import viewsets
from .models import User, Product, Cart, Order, OrderItem

from .serializers import (
    UserSerializer,
    ProductSerializer,
    CartSerializer,
    OrderSerializer,
    OrderItemSerializer,
)


from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Product, Cart, Order, OrderItem
from .serializers import (
    ProductSerializer,
    CartSerializer,
    OrderSerializer,
    OrderItemSerializer,
)


# Список товаров и просмотр деталей
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


# Корзина
class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    # Добавление товара в корзину
    def create(self, request):
        user_id = request.data.get("user_id")
        product_id = request.data.get("product")
        quantity = int(request.data.get("quantity", 1))

        cart_item, created = Cart.objects.get_or_create(
            user_id=user_id, product_id=product_id, defaults={"quantity": quantity}
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        return Response(CartSerializer(cart_item).data, status=status.HTTP_201_CREATED)

    # Удаление товара из корзины
    def destroy(self, request, pk=None):
        try:
            cart_item = Cart.objects.get(id=pk)
            cart_item.delete()
            return Response(
                {"detail": "Товар успешно удален из корзины."},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Cart.DoesNotExist:
            return Response(
                {"error": "Товар в корзине не найден."},
                status=status.HTTP_404_NOT_FOUND,
            )


# Заказы
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    # Оформление заказа
    def create(self, request):
        user_id = request.data.get("user_id")
        cart_items = Cart.objects.filter(user_id=user_id)

        if not cart_items:
            return Response(
                {"error": "Корзина пуста."}, status=status.HTTP_400_BAD_REQUEST
            )

        total_price = sum(item.product.price * item.quantity for item in cart_items)

        order = Order.objects.create(user_id=user_id, total_price=total_price)

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price,
            )
            item.delete()  # Очистка корзины после оформления заказа

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

    # Изменение статуса заказа (для админа)
    def partial_update(self, request, pk=None):
        order = self.get_object()
        status = request.data.get("status")

        if status not in ["Ожидает", "Подтвержден", "Отменен"]:
            return Response(
                {"error": "Неверный статус."}, status=status.HTTP_400_BAD_REQUEST
            )

        order.status = status
        order.save()

        return Response(OrderSerializer(order).data)
