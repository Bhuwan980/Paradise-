from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View, CreateView, FormView, ListView, DetailView
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CheckoutForm, CustomerRegistrationForm, CustomerLoginForm
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import  Q


# Create your views here.

#customer asign to the cart ogject
class EconMixin(object):
    def dispatch(self, request, *args, **kwargs):
        cart_id = request.session.get('cart_id', None)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            if request.user.is_authenticated and request.user.customer:
                cart_obj.customer = request.user.customer
                cart_obj.save()
        return super().dispatch(request, *args, **kwargs)


class HomeView(EconMixin, TemplateView):
    template_name = 'index.html'
    paginate_by = 5


    def get_context_data(self, *args, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['products'] = Product.objects.all().order_by('-id')
        context['category'] = Category.objects.all()
        return context

    # def get_context_data(self, **kwargs):
    #     context = super(HomeView, self).get_context_data(**kwargs)
    #     context['all_products'] = Product.objects.all()
    #     return context

# class LoginRequiredMixin(object):
#
#     @classmethod
#     def as_view(cls):
#         return login_required(super(LoginRequiredMixin, cls).as_view())




class ContactusView(EconMixin,LoginRequiredMixin, TemplateView):
    login_url = '/customer-login/'

    template_name = 'contactus.html'


class AboutView(EconMixin, TemplateView):
    redirect_field_name = 'redirect_to'
    template_name = 'about.html'


class AllProductsView(EconMixin, TemplateView):
    template_name = 'allproducts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['allcategories'] = Category.objects.all()
        return context


class ProductDetailView(EconMixin, TemplateView):
    template_name = 'productdetail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = kwargs['slug']
        product = Product.objects.get(slug=slug)
        product.count_view += 1
        product.save()
        context['product'] = product
        return context


class AddToCartView(EconMixin, TemplateView):
    template_name = "addtocart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get product id from requested url
        product_id = self.kwargs['pro_id']
        # get product
        product_obj = Product.objects.get(id=product_id)

        # check if cart exists
        cart_id = self.request.session.get("cart_id", None)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            this_product_in_cart = cart_obj.cartproduct_set.filter(
                product=product_obj)

            # item already exists in cart
            if this_product_in_cart.exists():
                cartproduct = this_product_in_cart.last()
                cartproduct.quantity += 1
                cartproduct.subtotal += product_obj.price
                cartproduct.save()
                cart_obj.total += product_obj.price
                cart_obj.save()
            # new item is added in cart
            else:
                cartproduct = CartProduct.objects.create(
                    cart=cart_obj, product=product_obj, rate=product_obj.price, quantity=1,
                    subtotal=product_obj.price)

                cart_obj.total += product_obj.price
                cart_obj.save()

        else:
            cart_obj = Cart.objects.create(total=0)
            self.request.session['cart_id'] = cart_obj.id
            cartproduct = CartProduct.objects.create(
                cart=cart_obj, product=product_obj, rate=product_obj.price, quantity=1,
                subtotal=product_obj.price)
            cart_obj.total += product_obj.price
            cart_obj.save()

        return context


class MyCartView(EconMixin, TemplateView):
    template_name = 'mycart.html'

    def get_context_data(self, **kwargs):
        cart_id = self.request.session.get('cart_id', None)
        context = super().get_context_data(**kwargs)
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
            context['cart'] = cart
        return context


class ManageCartView(EconMixin, View):

    def get(self, request, *args, **kwargs):
        cp_id = self.kwargs['id']
        action = request.GET.get('action')
        cp_obj = CartProduct.objects.get(id=cp_id)
        cart_obj = cp_obj.cart

        if action == 'inc':
            cp_obj.subtotal += cp_obj.rate
            cp_obj.quantity += 1
            cp_obj.save()
            cart_obj.total += cp_obj.rate
            cart_obj.save()

        elif action == 'dec':

            cp_obj.subtotal -= cp_obj.rate
            cp_obj.quantity -= 1
            cp_obj.save()
            cart_obj.total -= cp_obj.rate
            cart_obj.save()
            if cp_obj.quantity == 0:
                cp_obj.delete()
        else:
            cart_obj.total -= cp_obj.subtotal
            cart_obj.save()
            cp_obj.delete()
        return redirect('mycart')


class EmptyCartView(EconMixin, View):

    def get(self, request, *args, **kwargs):
        cart_id = request.session.get("cart_id", None)
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
            cart.cartproduct_set.all().delete()
            cart.total = 0
            cart.save()

        return redirect('mycart')


class CheckoutView(LoginRequiredMixin, EconMixin,CreateView):
    login_url = '/customer-login/'
    redirect_field_name = '/check-out/'

    print("33333333333333333333333333333333333333333", redirect_field_name)

    template_name = 'checkout.html'
    form_class = CheckoutForm
    success_url = reverse_lazy('home')


    # @method_decorator(login_required)
    # def dispatch(self, *args, **kwargs):
    #     return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CheckoutView, self).get_context_data(**kwargs)
        cart_id = self.request.session.get('cart_id', None)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
        context['cart'] = cart_obj
        return context

    def form_valid(self, form):
        cart_id = self.request.session.get('cart_id')
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            form.instance.cart = cart_obj
            form.instance.subtotal = cart_obj.total
            form.instance.total = cart_obj.total
            form.instance.order_status = 'Order Recieved'
            form.instance.discount = 0
            del self.request.session['cart_id']

        return super().form_valid(form)


class CustomerRegistrationView(CreateView):
    template_name = 'customerregistration.html'
    form_class = CustomerRegistrationForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        email = form.cleaned_data.get('email')
        user = User.objects.create_user(username=username, password=password, email=email)
        form.instance.user = user
        usr = authenticate(username=username, password=password)
        login(self.request, usr)
        return super().form_valid(form)




class CustomerLogoutView(View):

    def get(self, request):
        logout(request)
        return redirect('home')


class CustomerLoginView(FormView):
    template_name = 'customerlogin.html'
    form_class = CustomerLoginForm
    success_url = reverse_lazy('home')

    # form valid is type of post method which is available in createview, formview and updateveiw
    def form_valid(self, form):
        uname = form.cleaned_data['username']
        pswd = form.cleaned_data['password']
        user = authenticate(username=uname, password=pswd)

        if user is not None and user.customer:
            login(self.request, user)
        else:
            return render(self.request, self.template_name,
                          {'form': self.form_class, 'error': 'please enter valid credentials'})

        return super().form_valid(form)


class CustomerProfileView(LoginRequiredMixin, TemplateView):
    login_url = '/customer-login/'

    template_name = 'customerprofile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated and self.request.user.customer:
            context['user'] = self.request.user
            context['customer'] = self.request.user.customer
            context['order'] = Order.objects.filter(cart__customer=context['customer'])
        return context

class CustomerOrderDetailView(DetailView):
    template_name = 'order_detail_view.html'
    model = Order
    context_object_name = 'order_obj'


    def dispatch(self, request, *args, **kwargs):


        if request.user.is_authenticated and request.user.customer:
            order_id = self.kwargs['pk']
            order_obj = Order.objects.get(id=order_id)
            if request.user.customer != order_obj.cart.customer:
                return redirect('customerprofile')
        else:
            return redirect('customer-login/?next=/customer-profile/')

        return super().dispatch(request, *args, **kwargs)

class SearchResultView(TemplateView):
    template_name = 'searchresult.html'
    model = Product

    # def get_queryset(self):
    #     search_query = self.kwargs.get('search')
    #     object_list = self.model.objects.all()
    #     if search_query:
    #         result = object_list.filter(name__icontains=search_query)
    #
    #         print("########################################3", search_query)
    #     return result
    #
    # # search_post = srequest.GET.get('search')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('search')
        print('3333333333333333333333333333333333333333333333333333333333333333333333333',query)
        # context['result'] = Product.objects.filter(name=query)

        context['result'] =  Product.objects.filter(name__contains=query)

        return context
