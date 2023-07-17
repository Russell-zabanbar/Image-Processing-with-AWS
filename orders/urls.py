from django.urls import path
from orders.views import DetectFaceView, AddOrderView, AvailableOrderView

app_name = 'detect'
urlpatterns = [
    path('order_list/', DetectFaceView.as_view(), name='order_list'),
    path('add_order/', AddOrderView.as_view(), name='add_order'),
    path('available_order/', AvailableOrderView.as_view(), name='available_order')

]