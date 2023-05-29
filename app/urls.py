from django.urls import include, path
from rest_framework import routers
from .views import MemberViewSet, ReadingViewSet, InvoiceViewSet

router = routers.DefaultRouter()
router.register('members', MemberViewSet)
router.register('readings', ReadingViewSet)
router.register('invoices', InvoiceViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
