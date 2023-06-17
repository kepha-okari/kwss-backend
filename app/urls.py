
from django.urls import path
from .views import MemberAPIView, MemberDetailAPIView, MeterAPIView, MeterDetailAPIView, InvoiceListAPIView, InvoiceDetailAPIView, ReadingListAPIView, ReadingDetailAPIView

urlpatterns = [

    path('members/', MemberAPIView.as_view(), name='member-list'),
    path('members/<int:pk>/', MemberDetailAPIView.as_view(), name='member-detail'),
    path('meters/', MeterAPIView.as_view(), name='meter-list'),
    path('meters/<int:pk>/', MeterDetailAPIView.as_view(), name='meter-detail'),
    path('invoices/', InvoiceListAPIView.as_view(), name='invoice-list'),
    path('invoices/<int:pk>/', InvoiceDetailAPIView.as_view(), name='invoice-detail'),
    path('readings/', ReadingListAPIView.as_view(), name='reading-list'),
    path('readings/<int:pk>/', ReadingDetailAPIView.as_view(), name='reading-detail'),

]

