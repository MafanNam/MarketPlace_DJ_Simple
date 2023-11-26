from django.utils.timezone import now

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter

from orders.api.paginations import OrderAPIListPagination
from orders.api.serializers import (
    OrderSerializer, CreateOrderSerializer,
    UpdateOrderSerializer)
from orders.models import Order


class OrderViewSet(viewsets.ModelViewSet):
    """Order view"""
    http_method_names = ['get', 'post', 'patch', 'delete']
    pagination_class = OrderAPIListPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('order_number', 'status')
    ordering_fields = (
        'user', 'shipping_price', 'total_price',
        'tax', 'status', 'created_at',)

    def get_permissions(self):
        if self.request.method in ['PATCH']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        context = {'user': self.request.user}
        serializer = CreateOrderSerializer(
            data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        serializer = OrderSerializer(order)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all().order_by('-created_at').select_related(
                'user', 'tax').prefetch_related(
                'order_item', 'order_item__product', 'address')
        return Order.objects.filter(user=user).order_by(
            '-created_at').select_related('user', 'tax').prefetch_related(
            'order_item', 'order_item__product', 'address')

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateOrderSerializer
        elif self.request.method == 'PATCH':
            return UpdateOrderSerializer
        return OrderSerializer


class OrderPayViewSet(viewsets.views.APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = None

    def patch(self, request, pk=None):
        try:
            order = Order.objects.get(
                pk=pk, user=self.request.user)
        except Order.DoesNotExist:
            return Response(
                {'error': 'Order with this id does not exist.'},
                status=status.HTTP_404_NOT_FOUND)
        if not order.is_paid:
            order.is_paid = True
            order.paid_at = now()
            order.save()
        else:
            return Response({'error': 'Order already paid.'})

        return Response('Order was paid.')


class OrderDeliverViewSet(viewsets.views.APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = None

    def patch(self, request, pk=None):
        try:
            order = Order.objects.get(
                pk=pk, user=self.request.user)
        except Order.DoesNotExist:
            return Response(
                {'error': 'Order with this id does not exist.'},
                status=status.HTTP_404_NOT_FOUND)
        if not order.is_delivered:
            order.is_delivered = True
            order.delivered_at = now()
            order.save()
        else:
            return Response({'error': 'Order already delivered.'})

        return Response('Order was delivered.')
