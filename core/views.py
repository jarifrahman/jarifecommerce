from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, View, TemplateView
from django.shortcuts import redirect, render
from django.utils import timezone
from .forms import CheckoutForm, CouponForm, RefundForm
from .models import Item, OrderItem, Order, BillingAddress, Payment, Coupon, Refund, Category, Video, ProductHit
from django.http import HttpResponseRedirect
from .serializers import ItemSerializer, OrderSerializer, OrderItemSerializer, CategorySerializer
from rest_framework import generics, status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from django.db.models import Q
import requests
from rest_framework.test import APIClient
from twilio.rest import Client
from django.core.files.storage import FileSystemStorage
from .forms import VideoForm
from .serializers import VideoSerializer
import redis

from .permissions import IsAuthorOrReadOnly

# Create your views here.
import random
import string
import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))


## usage of forms
def showvideo(request):
    video= Video.objects
    ## using forms.py
    form= VideoForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()         
    context= {'video': video,
              'form': form
              }
    
      
    return render(request, 'video.html', context)


class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    #  authentication_classes=(TokenAuthentication, )
    # permission_classes = (IsAuthenticated )


class PaymentView(View):
    def get(self, *args, **kwargs):
        # order
        order = Order.objects.get(user=self.request.user, ordered=False)
        if order.billing_address:
            context = {
                'order': order,
                'DISPLAY_COUPON_FORM': False
            }
            return render(self.request, "payment.html", context)
        else:
            messages.warning(
                self.request, "u have not added a billing address")
            return redirect("core:checkout")

    def post(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        token = self.request.POST.get('stripeToken')
        amount = int(order.get_total() * 100)
        try:
            ## change keys in html page
            charge = stripe.Charge.create(
                amount=500,  # cents
                currency="usd",
                source=token,

            )
            # create the payment
            payment = Payment()
            payment.stripe_charge_id = charge['id']
            payment.user = self.request.user
            payment.amount = order.get_total()
            payment.phone = order.get_phone()
            payment.payafterdelivery = False
            
            payment.save()




            # assign the payment to the order
            order.ordered = True
            order.payment = payment
            # TODO : assign ref code
            order.ref_code = create_ref_code()
            order.save()

            # twilio setup, make sure values are also in settings.py
            account_sid = "ACc9d90a750508d1587a60d33176e04fea"
            # Your Auth Token from twilio.com/console
            auth_token  = "f471d37c55a6f4cf47f3d8893e9378ac"

            client = Client(account_sid, auth_token)
            client_phone_number = order.get_phone()
            message = client.messages.create(
                to=str(client_phone_number), 
                from_="+13344878514",
                body="your new order was succesful!")


            messages.success(self.request, ("your order was succesful, and card payment was succesful"))
            return redirect("/")

        except stripe.error.CardError as e:
            # Since it's a decline, stripe.error.CardError will be caught
            body = e.json_body
            err = body.get('error', {})
            messages.error(self.request, f"{err.get('message')}")
            return redirect("/")

        except stripe.error.RateLimitError as e:
            # Too many requests made to the API too quickly
            messages.error(self.request, "RateLimitError")
            return redirect("/")

        except stripe.error.InvalidRequestError as e:
            # Invalid parameters were supplied to Stripe's API
            messages.error(self.request, "Invalid parameters")
            return redirect("/")

        except stripe.error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            messages.error(self.request, "Not Authentication")
            return redirect("/")

        except stripe.error.APIConnectionError as e:
            # Network communication with Stripe failed
            messages.error(self.request, "Network Error")
            return redirect("/")

        except stripe.error.StripeError as e:
            # Display a very generic error to the user, and maybe send
            # yourself an email
            messages.error(self.request, "Something went wrong")
            return redirect("/")

        except Exception as e:
            # send an email to ourselves
            messages.error(self.request, "Serious Error occured")
            return redirect("/")

def createpayment2(request):
    order = Order.objects.get(user=request.user, ordered=False)
    if request.method =='POST':
        
        payment=Payment()
        payment.user = request.user
        payment.amount=order.get_total()
        payment.phone= order.get_phone()
        payment.payafterdelivery = True
        payment.save()
        order.ordered = True
        order.payment = payment
        # TODO : assign ref code
        order.ref_code = create_ref_code()
        order.save()
        return redirect('/')
    
    else:
            return render(request,'payment2.html')

# count number of clicks/ count number of product clicks// use on detailview or view
def clickup(request):
    item = Item.objects.all()
    if request.method =='POST':
        product_hit=ProductHit()
        print(request.user)
        product_hit.user = request.user
        product_hit.items=request.POST['productname']
        product_hit.hits = +1
        product_hit.save()
        #order.ordered = True
        #order.payment = payment
        # TODO : assign ref code
       # order.ref_code = create_ref_code()
       # order.save()
        return redirect('/')
    
    else:
            return render(request,'payment2.html')


class HomeView(ListView):
    template_name = "index.html"
    queryset = Item.objects.filter(is_active=True)
    context_object_name = 'items'


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'order_summary.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect("/")

# cannot have post in listview
class ShopView(ListView):
    model = Item
    paginate_by = 6
    template_name = "shop.html"


class OrderItemPView(TemplateView):
    template_name = 'order2s.html'

class OrderItemView(ListView):
    model = OrderItem
    paginate_by = 6
    template_name = "order2.html"
    def get_queryset(self): # new
            query = self.request.GET.get('q')
            username = self.request.user.username
           # object_list = OrderItem.objects.all()
            object_list = OrderItem.objects.filter(
                Q(user__username__icontains=username)
            )
            return object_list

class OrderView(ListView):
    model = Order
    paginate_by = 6
    template_name = "order1.html"
    def get_queryset(self): # new
            query = self.request.GET.get('q')
            object_list = Order.objects.filter(
                Q(user__username__icontains='admin')
            )
            return object_list


class ItemDetailView(DetailView):
    model = Item
    template_name = "product-detail.html"



class VideoDetailView(DetailView):
    model = Video
    template_name = "video-detail.html"


# class CategoryView(DetailView):
#     model = Category
#     template_name = "category.html"

class CategoryView(View):
    def get(self, *args, **kwargs):
        category = Category.objects.get(slug=self.kwargs['slug'])
        item = Item.objects.filter(category=category, is_active=True)
        context = {
            'object_list': item,
            'category_title': category,
            'category_description': category.description,
            'category_image': category.image
        }
        return render(self.request, "category.html", context)


class CategoryVideoView(View):
    def get(self, *args, **kwargs):
        category = Category.objects.get(slug=self.kwargs['slug'])
        video = Video.objects.filter(category=category)
        context = {
            'object_list': video,
            'category_title': category,
            'category_description': category.description,
            'category_image': category.image
        }
        return render(self.request, "videocategory.html", context)


class CheckoutView(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            form = CheckoutForm()
            context = {
                'form': form,
                'couponform': CouponForm(),
                'order': order,
                'DISPLAY_COUPON_FORM': True
            }
            return render(self.request, "checkout.html", context)

        except ObjectDoesNotExist:
            messages.info(self.request, "You do not have an active order")
            return redirect("coreInvalid parameters:checkout")

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            print(self.request.POST)
            if form.is_valid():
                street_address = form.cleaned_data.get('street_address')
                apartment_address = form.cleaned_data.get('apartment_address')
                country = form.cleaned_data.get('country')
                zip = form.cleaned_data.get('zip')
                phone = form.cleaned_data.get('phone')
                payafter = form.cleaned_data.get('payafter')
                # add functionality for these fields
                # same_shipping_address = form.cleaned_data.get(
                #     'same_shipping_address')
                # save_info = form.cleaned_data.get('save_info')
                payment_option = form.cleaned_data.get('payment_option')
                billing_address = BillingAddress(
                    user=self.request.user,
                    street_address=street_address,
                    apartment_address=apartment_address,
                    country=country,
                    zip=zip,
                    address_type='B'
                )
                billing_address.save()
                order.billing_address = billing_address
                order.phone = phone
                order.payafter = payafter
                order.save()

                # add redirect to the selected payment option
                if payment_option == 'S':
                    return redirect('core:payment', payment_option='stripe')
                elif payment_option == 'P':
                    return redirect('core:payment', payment_option='paypal')
                else:
                    messages.warning(
                        self.request, "Invalid payment option select")
                    return redirect('core:checkout')
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect("core:order-summary")






# def home(request):
#     context = {
#         'items': Item.objects.all()
#     }
#     return render(request, "index.html", context)
#
#
# def products(request):
#     context = {
#         'items': Item.objects.all()
#     }
#     return render(request, "product-detail.html", context)
#
#
# def shop(request):
#     context = {
#         'items': Item.objects.all()
#     }
#     return render(request, "shop.html", context)


@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "Item qty was updated.")
            return redirect("core:order-summary")
        else:
            order.items.add(order_item)
            messages.info(request, "Item was added to your cart.")
            return redirect("core:order-summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "Item was added to your cart.")
    return redirect("core:order-summary")


@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            messages.info(request, "Item was removed from your cart.")
            return redirect("core:order-summary")
        else:
            # add a message saying the user dosent have an order
            messages.info(request, "Item was not in your cart.")
            return redirect("core:product", slug=slug)
    else:
        # add a message saying the user dosent have an order
        messages.info(request, "u don't have an active order.")
        return redirect("core:product", slug=slug)
    return redirect("core:product", slug=slug)



## vote for product in detail view
@login_required
def productvote(request, slug):
    item = get_object_or_404(Item, slug=slug)
    item.votes_total += 1
    item.save()
    return redirect("/")
        


@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item qty was updated.")
            return redirect("core:order-summary")
        else:
            # add a message saying the user dosent have an order
            messages.info(request, "Item was not in your cart.")
            return redirect("core:product", slug=slug)
    else:
        # add a message saying the user dosent have an order
        messages.info(request, "u don't have an active order.")
        return redirect("core:product", slug=slug)
    return redirect("core:product", slug=slug)


def get_coupon(request, code):
    try:
        coupon = Coupon.objects.get(code=code)
        return coupon
    except ObjectDoesNotExist:
        messages.info(request, "This coupon does not exist")
        return redirect("core:checkout")


class AddCouponView(View):
    def post(self, *args, **kwargs):
        form = CouponForm(self.request.POST or None)
        if form.is_valid():
            try:
                code = form.cleaned_data.get('code')
                order = Order.objects.get(
                    user=self.request.user, ordered=False)
                order.coupon = get_coupon(self.request, code)
                order.save()
                messages.success(self.request, "Successfully added coupon")
                return redirect("core:checkout")

            except ObjectDoesNotExist:
                messages.info(request, "You do not have an active order")
                return redirect("core:checkout")


class RequestRefundView(View):
    def get(self, *args, **kwargs):
        form = RefundForm()
        context = {
            'form': form
        }
        return render(self.request, "request_refund.html", context)

    def post(self, *args, **kwargs):
        form = RefundForm(self.request.POST)
        if form.is_valid():
            ref_code = form.cleaned_data.get('ref_code')
            message = form.cleaned_data.get('message')
            email = form.cleaned_data.get('email')
            # edit the order
            try:
                order = Order.objects.get(ref_code=ref_code)
                order.refund_requested = True
                order.save()

                # store the refund
                refund = Refund()
                refund.order = order
                refund.reason = message
                refund.email = email
                refund.save()

                messages.info(self.request, "Your request was received")
                return redirect("core:request-refund")

            except ObjectDoesNotExist:
                messages.info(self.request, "This order does not exist")
                return redirect("core:request-refund")




class ItemViewSet(viewsets.ModelViewSet):
    """Provide CRUD +L functionality for Question."""
    queryset = Item.objects.all().order_by("-category")
    lookup_field = "slug"
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class OrderViewSet(viewsets.ModelViewSet):
    """Provide CRUD +L functionality for Question."""
    queryset = Order.objects.all().order_by("-user")
    lookup_field = "ref_code"
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class OrderItemViewSet(viewsets.ModelViewSet):
    """Provide CRUD +L functionality for Question."""
    queryset = OrderItem.objects.all().order_by("-item")
    lookup_field = "item"
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CategoryViewSet(viewsets.ModelViewSet):
    """Provide CRUD +L functionality for Question."""
    queryset = Category.objects.all().order_by("-title")
    lookup_field = "title"
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

# enable authentication of api
class CategoryAPIList(APIView):
    def get(self, request):
        category = Category.objects.all().order_by("-title")
        serializer = CategorySerializer(category, many=True)
        return Response(serializer.data) 
    def post(self):
        pass

# get json from rest api and use it
def categoryapi(request):
    response = requests.get('http://127.0.0.1:8000/categoryapi/')
    categorydata = response.json()
    titles =[]
    descriptions= []
    images = []
    for a in categorydata:
        titles.append(a['title'])
        descriptions.append(a['description'])
        images.append(a['image'])
    return render(request, 'categoryapi.html', {
        'categorydata': categorydata,
        'titles': titles,
        'descriptions': descriptions,
        'images': images,  })




def pornapi(request):
    mytoken = "250cc0b422a2315f62014f96d9864035640851c6"
    response = requests.get('http://192.168.1.206:8000/api/products/', headers={'Authorization': 'Token {}'.format(mytoken)})
    categorydata = response.json()
    
    titles =[]
    descriptions= []
    images = []
    for a in categorydata:
        titles.append(a['title'])
        descriptions.append(a['description'])
        images.append(a['image'])
    return render(request, 'categoryapi.html', {
        'categorydata': categorydata,
        'titles': titles,
        'descriptions': descriptions,
        'images': images,  })
       
 



class Csearchpage(TemplateView):
    template_name = 'csearch.html'


class Csearch(ListView):
    model = Item
    template_name = 'csearch.html'
    

    def get_queryset(self): # new
            query = self.request.GET.get('q')
            object_list = Item.objects.filter(
               Q(title__icontains=query)
            )
            return object_list




    

