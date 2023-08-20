from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q, Sum
from .utiles.utils import get_single_object
from .models import Medicine, Manufacturer, Order

@login_required(login_url='/login-user')
def index(request):
    return render(request, 'index.html')

@login_required(login_url='/login-user')
def dashboard(request):

    total_medicine_count = Medicine.objects.count()
    total_orders = Order.objects.count()
    total_order_delivered = Order.objects.filter(status='delivered').count()
    total_order_amount = Order.objects.aggregate(total_amount=Sum('total_amount'))['total_amount']

    print(total_medicine_count)

    context = {
        'total_medicine_count': total_medicine_count,
        'total_orders': total_orders,
        'total_order_amount': total_order_amount,
        'total_order_delivered': total_order_delivered,
    }
    return render(request, 'dashboard.html', context)

# manufacturer section
@login_required(login_url='/login-user')
def manufacturers(request):

    manufacturers = Manufacturer.objects.all()

    context = {
        'manufacturers': manufacturers
    }

    return render(request, 'manufacturer/manufacturers.html', context)

@login_required(login_url='/login-user')
def remove_manufacturer(request, pk):

    try:
        object = Manufacturer.objects.get(pk=pk)
        object.delete()
        messages.success(request, f"{object.name} removed successfully from manufacturer list")
        return redirect(request.META.get('HTTP_REFERER'))
    except:
        messages.warning(request, "Something went wrong")
        return redirect(request.META.get('HTTP_REFERER'))

    return redirect('manufacturers')

@login_required(login_url='/login-user')
def add_manufacturer(request):

    if request.method == 'POST':
        manufacturer_name = request.POST['manufacturer_name']
        contact_info = request.POST['contact_info']
        address = request.POST['address']

        if manufacturer_name and contact_info and address:
            object = Manufacturer.objects.create(
                name=manufacturer_name,
                address=address,
                contact_info=contact_info
            )
            messages.success(request, "Successfully created new manufacutrer")
            # return redirect('manufacturers')
        else:
            messages.warning(request, 'Something went wrong')

    return render(request, 'manufacturer/add-manufacturer.html')

@login_required(login_url='/login-user')
def edit_manufacturer(request, pk):

    try:
        object = Manufacturer.objects.get(pk=pk)

        if request.method == 'POST':
            manufacturer_name = request.POST['manufacturer_name']
            contact_info = request.POST['contact_info']
            address = request.POST['address']

            if manufacturer_name and contact_info and address:
                object.name = manufacturer_name
                object.address = address
                object.contact_info = contact_info
                object.save()
                messages.success(request, f"{object.name} has been updated successfully")
    except:
        messages.warning(request, "Something went wrong")

    context = {
        'object': object
    }

    return render(request, "manufacturer/edit-manufacturer.html", context)


# medicine section
@login_required(login_url='/login-user')
def add_new_medicine(request):

    manufacturers = Manufacturer.objects.all()

    if request.method == 'POST':
        name = request.POST['name']
        manufacturer_pk = request.POST['manufacturer_name']
        price = request.POST['price']
        stock_quantity = request.POST['stock_quantity']
        production_date = request.POST['production_date']
        expiration_date = request.POST['expiration_date']
        active_ingradients = request.POST['active_ingradients']
        storage_instruction = request.POST['storage_instruction']
        usage_instructionos = request.POST['usage_instructionos']
        precautions = request.POST['precautions']
        is_prescription_required = request.POST.get('is_prescription_required')
        dosage = request.POST['dosage']
        description = request.POST['description']
        image = request.FILES['image']

        if name and manufacturer_pk and price and stock_quantity and production_date and active_ingradients and storage_instruction and usage_instructionos and dosage and description:
            try:
                manufacturer_object = Manufacturer.objects.get(pk=manufacturer_pk)

                medicine = Medicine.objects.create(
                    name=name,
                    manufacturer=manufacturer_object,
                    production_date=production_date,
                    expiration_date=expiration_date,
                    price=price,
                    quantity_in_stock=stock_quantity,
                    dosage=dosage,
                    active_ingredients=active_ingradients,
                    storage_instructions=storage_instruction,
                    usage_instructions=usage_instructionos,
                    image=image,
                    description=description
                )
                if precautions:
                    medicine.precautions = precautions
                    medicine.save()
                if is_prescription_required:
                    medicine.is_prescription_required = True
                    medicine.save()

                messages.success(request, "New medicine has been added successfully")
                return redirect(request.META.get('HTTP_REFERER'))
            except:
                messages.warning(request, "Something went wrong")
                return redirect(request.META.get('HTTP_REFERER'))

    context = {
        'manufacturers': manufacturers
    }

    return render(request, 'medicine/add-new-medicine.html', context)

@login_required(login_url='/login-user')
def mark_as_expired(request, pk):

    try:
        object = get_object_or_404(Medicine, pk=pk)
        if object.is_expired:
            object.is_expired=False
            object.save()
        else:
            object.is_expired = True
            object.save()
        object.save()
        messages.success(request, "Successfully marked as expired")
        return redirect(request.META.get('HTTP_REFERER'))
    except:
        messages.warning(request, "Something went wrong")
        return redirect(request.META.get('HTTP_REFERER'))

    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='/login-user')
def remove_medicine_item(request, pk):
    fs = FileSystemStorage()
    try:
        object = Medicine.objects.get(pk=pk)
        fs.delete(object.image.name)
        object.delete()
        messages.success(request, "Successfully removed item")
        return redirect(request.META.get('HTTP_REFERER'))
    except:
        messages.warning(request, "Something went wrong")
        return redirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='/login-user')
def edit_medicine_item(request, pk):

    manufacturer = Manufacturer.objects.all()

    try:
        object = Medicine.objects.get(pk=pk)
        fs = FileSystemStorage()

        if request.method == 'POST':
            name = request.POST['name']
            manufacturer_pk = request.POST['manufacturer_name']
            price = request.POST['price']
            stock_quantity = request.POST['stock_quantity']
            production_date = request.POST['production_date']
            expiration_date = request.POST['expiration_date']
            active_ingradients = request.POST['active_ingradients']
            storage_instruction = request.POST['storage_instruction']
            usage_instructionos = request.POST['usage_instructionos']
            precautions = request.POST.get('precautions')
            is_prescription_required = request.POST.get('is_prescription_required')
            dosage = request.POST['dosage']
            description = request.POST['description']


            if name and manufacturer_pk and price and stock_quantity and production_date and active_ingradients and storage_instruction and usage_instructionos and dosage and description:
                try:
                    manufacturer_object = Manufacturer.objects.get(pk=manufacturer_pk)

                    object.name = name
                    object.manufacturer = manufacturer_object
                    object.production_date = production_date
                    object.expiration_date = expiration_date
                    object.price = price
                    object.quantity_in_stock = stock_quantity
                    object.dosage = dosage
                    object.active_ingredients = active_ingradients
                    object.storage_instructions = storage_instruction
                    object.usage_instructions = usage_instructionos
                    object.description = description
                    object.save()
                    try:
                        image = request.FILES['image']
                        fs.delete(object.image.name)
                        object.image = image
                        object.save()
                    except:
                        pass
                    if precautions:
                        object.precautions = precautions
                        object.save()
                    if is_prescription_required:
                        object.is_prescription_required = True
                        object.save()

                    messages.success(request, "New medicine has been added successfully")
                    return redirect(request.META.get('HTTP_REFERER'))
                except:
                    messages.warning(request, "Something went wrong")
                    return redirect(request.META.get('HTTP_REFERER'))

    except:
        messages.warning(request, "Something went wrong")

    context = {
        'object': object,
        'pk': pk,
        'manufacturers': manufacturer
    }

    return render(request, 'medicine/edit-medicine.html', context)

def active_medicine_list(request):

    medicine_list = Medicine.objects.filter(is_expired=False)

    context = {
        'medicine_list': medicine_list
    }

    return render(request, 'medicine/active-medicine-list.html', context)

def expired_medicine_list(request):

    medicine_list = Medicine.objects.filter(is_expired=True)

    context = {
        'medicine_list': medicine_list
    }

    return render(request, 'medicine/expired-medicine-list.html', context)

# order section
def active_orders(request):

    active_order = Order.objects.filter(status="active")

    context = {
        'active_orders': active_order,
    }

    return render(request, 'orders/active-orders.html', context)

def delivered_orders(request):
    delivered_orders = Order.objects.filter(status="delivered")

    context = {
        'delivered_orders': delivered_orders,
    }

    return render(request, 'orders/delivered-orders.html', context)

def cancelled_orders(request):
    cancelled_orders = Order.objects.filter(status="cancelled")

    context = {
        'cancelled_orders': cancelled_orders,
    }

    return render(request, 'orders/cancelled-orders.html', context)

def mark_as_delivered_or_cancelled_or_active(request, pk, mark_status):

    try:
        object = Order.objects.get(pk=pk)
        if mark_status == 'delivered' or mark_status == 'cancelled' or mark_status == 'active':
            object.status=mark_status
            object.save()
        if mark_status == 'paid':
            object.isPaid=True
            object.save()
        if mark_status == 'unpaid':
            object.isPaid=False
            object.save()
        messages.success(request, f"Successfully marked as {mark_status}")
    except:
        messages.warning(request, "Something went wrong")

    return redirect(request.META.get('HTTP_REFERER'))

def invoice(request, pk):

    object = Order.objects.get(pk=pk)

    context = {
        'object': object,
    }

    return render(request, 'invoices/index.html', context)

def profile(request):

    return render(request, 'profile/profile.html')


def login_view(request):

    if request.method == 'POST':
        email_or_username = request.POST['username']
        password = request.POST['password']


        if email_or_username and password:
            try:
                user = User.objects.filter(Q(username=email_or_username) | Q(email=email_or_username)).first
                if user and user.is_active == True:
                    authenticate_user = authenticate(request, email=user.email, password=password)
                    if authenticate_user is not None:
                        login(request, authenticate_user)
                        return redirect('dashboard')
            except:
                messages.warning(request, "Account with this credetial is not activated yet!")
                return redirect('dashboard')

    return render(request, 'login/login.html')


def register_view(request):

    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']


        if first_name and last_name and username and email and password:
            try:
                user = User.objects.create_superuser(
                    first_name=first_name,
                    last_name=last_name,
                    username=username,
                    email=email,
                    password=password,
                )
                messages.success(request, "Your account has been created successfully")

            except:
                messages.warning(request, "Account with this credential is not activated yet!")

    return render(request, 'login/register.html')