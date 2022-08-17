from rest_framework_nested import routers

from . import views

router = routers.DefaultRouter()
router.register('collection', views.CollectionViewSet)
router.register('products', views.ProductViewSet, basename="product")
router.register('carts', views.CartViewSet, basename="cart")
router.register('customers', views.CustomerViewSet)
router.register('orders', views.OrderViewSet, basename="orders")
router.register('store', views.StoreViewSet, basename="stores")


product_router = routers.NestedSimpleRouter(router, 'products', lookup='product')
product_router.register('reviews', views.ReviewViewSet, basename="product-reviews")
product_router.register('images', views.ProductImageView, basename="product-images")

cart_router = routers.NestedSimpleRouter(router, 'carts', lookup='cart')
cart_router.register('items', views.CartItemViewSet, basename="cart-items")

urlpatterns = router.urls + product_router.urls + cart_router.urls
