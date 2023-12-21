from rest_framework.routers import DefaultRouter
from . import views


app_name = 'product'


router = DefaultRouter()
router.register('products', views.ProductViewSets, basename='product-api')
router.register(
    'product-log', views.ProductLogViewSets, basename='log-product-api'
)

urlpatterns = router.urls
