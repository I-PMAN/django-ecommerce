from django.shortcuts import render
from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from .models import Cart, CartItem, Order, Address
from .serializers import CartSerializer, CartItemSerializer, OrderSerializer, AddressSerializer
from .permissions import IsAdminOrOwner
import uuid
from rest_framework.views import APIView
from rest_framework.decorators import action

class CartView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return cart


class AddToCartView(generics.CreateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        product = serializer.validated_data['product']
        quantity = serializer.validated_Data['quantity']

        if product.stock < quantity:
            raise serializers.ValidationError(
                f"Only {product.stock} items left in stock."
            )

        serializer.save(cart=cart)

class UpdateCartItemView(generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        product = serializer.validated_data.get('product', serializer.instance.product)
        quantity = serializer.validated_data.get('quantity', serializer.instance.quantity)

        if product.stock < quantity:
            raise serializers.ValidationError(
                f"Only {product.stock} items left in stock."
            )
        
        serializer.save()

class PaymentSimulationView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            order = Order.objects.get(pk=pk, user=request.user)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        if order.status != "PENDING":
            return Response({"errors": "Order is not pending"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Checking stock
        for item in order.items.all():
            if item.product.stock < item.quantity:
                return Response(
                        {"error": f"Not enough stock for {item.product.name}"}, status=status.HTTP_400_BAD_REQUEST)
        
        
        for item in order.items.all():
            item.product.stock -= item.quantity
            item.product.save()

        payment_method = request.data.get("payment_method", "MockPay")
        transaction_id = str(uuid.uuid4())

        order.status = "PAID"
        order.payment_method = payment_method
        order.transaction_id = transaction_id
        order.save()

        return Response({
            "message": "Payment successful",
            "order_id": order.id,
            "status": order.status,
            "payment_method": order.payment_method,
            "transaction_id": order.transaction_id
            }, status=status.HTTP_200_OK)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('-created_at')
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrOwner]

    def get_queryset(self):
        if self.request.user.is_admin:
            return Order.objects.all().order_by('-created_at')
        return Order.objects.filter(user=self.request.user).order_by('-created_at')

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def update_status(self, request, pk=None):
        """Admins can update order status"""
        try:
            order = self.get_object()
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        if not request.user.is_admin:
            return Response({"error": "Only admins can update status"}, status=status.HTTP_403_FORBIDDEN)
        
        new_status = request.data.get("status")
        if new_status not in ["PAID", "SHIPPED", "DELIVERED", "CANCELLED"]:
            return Response({"error": "Invalid status"}, status=HTTP_400_BAD_REQUEST)

        order.status = new_status
        order.save()

        return Response({
            "message": f"Order status updated to {new_status}",
            "order_id": order.id,
            "status": order.status
            }, status=HTTP_200_OK)


class CheckoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        # Get the user's cart
        try:
            cart = Cart.objects.get(user.request.user)
        except Cart.DoesNotExist:
            return Response(
                {"error": "cart not found"}, status=status.HTTP_404_NOT_FOUND
                )

        cart_items = cart.items.all()
        if not cart_items.exists():
            return Response({"error": "Cart in empty"}, status=status.HTTP_400_BAD_REQUEST)

        
        # Get address
        address_id = request.data.get("address_id")
        if address_id:
            try:
                address = Address.objects.get(id=address_id, user=request.user)
            except Address.DoesNotExist:
                return Response({"error": "Invalid address"}, status=status.HTTP_404_NOT_FOUND)
        else:
            address = Address.objects.get(id=address_id, user=request.user, is_default=True).first()
            if not address:
                return Response({"error": "No default address found. Please add one."}, status=status.HTTP_400_BAD_REQUEST)
        
        
        # Calculate total
        total_price = sum(item.product.price * item.quantity for item in cart_items)

        # Create order
        order = Order.objects.create(
            user=request.user,
            total_price=total_price,
            status="PENDING"
        )

        # Add items form cart -> order
        for items in cart_items:
            order.items.create(product=item.product, quantity=item.quantity)

        cart_items.delete()

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class AddressListCreateView(generics.ListCreateAPIView):
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # If setting address as default, remove all other default addresses
        if serializer.validated_data.get('is_default', False):
            Address.objects.filter(user=self.request.user, is_default=True).update(is_default=False)
        serializer.save(user=self.request.user)
    
class AddressUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        if serializer.validated_data.get('is_default', False):
            Address.objects.filter(user=self.request.user, is_default=True).update(is_default=False)
        serializer.save()

class SetDefaultAddressView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            address = Address.objects.get(id=pk, user=request.user)
        except Address.DoesNotExist:
            return Response({"error": "Address not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # Unset old default
        Address.objects.filter(user=request.user, is_default=True).update(is_default=False)

        # Set new default
        address.is_default = True
        address.save()

        return Response({"message": "Default address set"}, status=status.HTTP_200_OK)