
from django.urls import path
from .views import MemberAPIView, MemberDetailAPIView

urlpatterns = [
    path('members/', MemberAPIView.as_view(), name='members'),
    path('members/<int:pk>/', MemberDetailAPIView.as_view(), name='member-detail'),
]

# from django.urls import path
# from .views import MemberAPIView

# urlpatterns = [
#     path('members/', MemberAPIView.as_view(), name='member-list'),
# ]


