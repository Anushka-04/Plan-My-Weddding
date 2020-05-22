from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View, DetailView
from .models import *
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.utils import timezone

# Create your views here.
class BaseView(View):
    template_context = {
    "vendors" : Vendor.objects.all()
    }

class HomeView(BaseView):
    def get(self, request):
        self.template_context["types"] = VendorType.objects.all()
        self.template_context["sliders"] = Slider.objects.all()
        return render(request, "index.html", self.template_context)

class VendorView(BaseView):
	def get(self, request):
		self.template_context["types"] = VendorType.objects.all()
		self.template_context["vendors"] = Vendor.objects.all()
		return render(request, "vendors.html", self.template_context)




class VendorDetailView(DetailView):
	model = Vendor
	template_name = "single-item.html"

	def get_context_data(self, **kwargs):
		context = super(VendorDetailView, self).get_context_data(**kwargs)
		types = VendorType.objects.all()
		context['types'] = types
		return context


def vendor_type_list(request, *args, **kwargs):
    type = kwargs.get('type_name')
    types = VendorType.objects.all()
    type_name = get_object_or_404(VendorType.objects.all(), type_name=type)
    #menus = Menu.objects.filter(type=type)
    return render(request,'vendorlist.html', {'type_name': type_name,'types':types})


def register(request):
    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        password1 = request.POST["password1"]
        if first_name and last_name and username and email and password and password1:
            try:
                validate_email(email)
            except ValidationError as e:
                print("bad email, details:", e)
                messages.error(request, "Invalid Email")
                return render(request, "register.html")
            else:
                print("good email")
                if password == password1:
                    if User.objects.filter(username = username).exists():
                        messages.error(request, "This UserName is already taken.")
                        return render(request, "register.html")
                    else:
                        if User.objects.filter(email=email).exists():
                            messages.error(request, "This Email is already taken.")
                            return render(request, "register.html")
                        else:
                            user = User.objects.create_user(
                                first_name=first_name,
                                last_name=last_name,
                                username=username,
                                email=email,
                                password=password
                            )
                            user.save()
                            messages.success(request, "You are registered.")
                            return redirect("/accounts/login")
                else:
                    messages.error(request, "Passwords doesnot match.")
                    return redirect("home:signup")
        else:
            messages.error(request,"Please fill all the fields.")
            return render(request,'register.html')
    return render(request,'register.html')




class AddSummary(BaseView):
    def get(self, *arg, **kwargs):
        try:
            add = Add.objects.get(
                user=self.request.user,
                added=False

            )
            self.template_context["object"] = add
            return render(self.request, "my_list.html", self.template_context)

        except ObjectDoesNotExist:
            messages.error(self.request, "Some Error Occured.")
            return redirect("/")




@login_required
def add_to_list(request, slug):
    vendor = get_object_or_404(Vendor, slug=slug)
    add_vendor = AddVendor.objects.get_or_create(
        vendor=vendor,
        user=request.user,
        added=False
    )[0]
    adds = Add.objects.filter(
        user=request.user,
        added=False
    )
    if adds.exists():
        add=adds[0]
        add.vendors.add(add_vendor)
        messages.info(request, "The vendor is updated in your cart.")
        return redirect("home:adds")
    else:
        add_date = timezone.now()
        add = Add.objects.create(
            user=request.user,
            added_date = add_date,
        )
        add.vendors.add(add_vendor)
        messages.info(request, "Vendor is added")
        return redirect("home:adds")

