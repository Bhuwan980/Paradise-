from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('contact-us/', ContactusView.as_view(), name='contactus'),

    path('about/', AboutView.as_view(), name='about'),

    path('all-categories/', AllProductsView.as_view(), name='allcategories'),
    path('product/<slug:slug>', ProductDetailView.as_view(), name='productdetail'),
    path('add-to-cart-<int:pro_id>/', AddToCartView.as_view(), name='addtocart'),
    path('my-cart/', MyCartView.as_view(), name='mycart'),
    path('manage-cart/<int:id>', ManageCartView.as_view(), name='managecart'),
    path('empty-cart', EmptyCartView.as_view(), name='emptycart'),

    path('check-out/', CheckoutView.as_view(), name='checkout'),

    path('customer-registration', CustomerRegistrationView.as_view(), name='customerregistration'),
    path('customer-logout/', CustomerLogoutView.as_view(), name='customerlogout'),
    path('customer-login/', CustomerLoginView.as_view(), name='customerlogin'),
    path('customer-profile/', CustomerProfileView.as_view(), name='customerprofile'),

    path('customer-profile/order-detail-<int:pk>/', CustomerOrderDetailView.as_view(), name='orderdetailview'),
    path('search-result/', SearchResultView.as_view(), name='searchresult'),

    path('create-product/', CreateProductView.as_view(), name='createproduct'),

]
