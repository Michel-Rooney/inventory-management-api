from rest_framework.routers import DefaultRouter
from . import views

app_name = 'purchase'

router = DefaultRouter()
router.register('purchase', views.PurchaseViewSets, basename='purchase-api')

urlpatterns = router.urls
