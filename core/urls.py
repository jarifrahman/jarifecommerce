from django.urls import path, include
from django.urls import path
from .views import (
    ItemDetailView,
    HomeView,
    add_to_cart,
    remove_from_cart,
    ShopView,
    OrderSummaryView,
    remove_single_item_from_cart,
    CheckoutView,
    PaymentView,
    AddCouponView,
    RequestRefundView,
    CategoryView,
    OrderView
    ,OrderItemView
, OrderItemPView
,Csearchpage,
Csearch,
CategoryAPIList,
categoryapi,
createpayment2,
pornapi,
showvideo,CategoryVideoView,
VideoDetailView,
clickup,
productvote
)
from rest_framework.routers import DefaultRouter

from . import views as qv

router = DefaultRouter()
router.register(r"items", qv.ItemViewSet)
router.register(r"orders", qv.OrderViewSet)
router.register(r"orderitems", qv.OrderItemViewSet)
router.register(r"categories", qv.CategoryViewSet)
router.register(r"videos", qv.VideoViewSet)


app_name = 'core'

urlpatterns = [
    
    path('', HomeView.as_view(), name='home'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('category/<slug>/', CategoryView.as_view(), name='category'),
    path('videocategory/<slug>/', CategoryVideoView.as_view(), name='videocategory'),   ##
    path('product/<slug>/', ItemDetailView.as_view(), name='product'),
    path('video/<slug>/', VideoDetailView.as_view(), name='video'),  ##
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('add_coupon/', AddCouponView.as_view(), name='add-coupon'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('productvote/<slug>/', productvote, name='productvote'),
    path('shop/', ShopView.as_view(), name='shop'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('remove-item-from-cart/<slug>/', remove_single_item_from_cart,
         name='remove-single-item-from-cart'),
    path('payment/<payment_option>/', PaymentView.as_view(), name='payment'),
    path('request-refund/', RequestRefundView.as_view(), name='request-refund'),
    path("api/", include(router.urls)), 
    path('orders/', OrderView.as_view(), name='order1'),
    path('orders2_result/', OrderItemView.as_view(), name='orders2_result'),
    path('orders2_page/', OrderItemPView.as_view(), name='orders2_page'),
    path('categoryapi/', CategoryAPIList.as_view(), name='categoryapi'),
    path('categoryapipage/', categoryapi, name='categoryapi1'),
    path('pornapipage/', pornapi, name='categoryapi1'),
    path('checkout/payment2/', createpayment2, name='payment2'),
    path('video/', showvideo, name='video'),  ##
    path('clickup/', clickup, name='clickup'),
   
]


