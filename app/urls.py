
from django.urls import path
from .views import MemberAPIView, MemberDetailAPIView, MeterAPIView, MeterDetailAPIView

urlpatterns = [
    path('members/', MemberAPIView.as_view(), name='member-list'),
    path('members/<int:pk>/', MemberDetailAPIView.as_view(), name='member-detail'),
    path('meters/', MeterAPIView.as_view(), name='meter-list'),
    path('meters/<int:pk>/', MeterDetailAPIView.as_view(), name='meter-detail'),
]



