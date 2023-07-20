from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.template.defaultfilters import slugify
from .forms import VendorForm
from accounts.forms import UserProfileForm
from accounts.models import UserProfile
from accounts.views import check_role_vendor
from .models import Vendor
from menu.models import Category, OnlineItem
from menu.forms import CategoryForm, OnlineItemForm


# Create your views here.
def get_vendor(request):
    vendor = Vendor.objects.get(user=request.user)
    return vendor


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vprofile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    vendor = get_object_or_404(Vendor, user=request.user)
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance = profile)
        vendor_form = VendorForm(request.POST, request.FILES, instance = vendor)
        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request, 'settings updated.')
            return redirect('vprofile')
        else:
            print(profile_form.errors)
            print(vendor_form.errors)
    else:         
        profile_form = UserProfileForm(instance = profile)
        vendor_form = VendorForm(instance = vendor)

    context = {
        'profile_form': profile_form,
        'vendor_form': vendor_form,
        'profile': profile,
        'vendor': vendor,
    }
    return render(request, 'home/vendor/vprofile.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def menu_builder(request):
    vendor = get_vendor(request)
    categories = Category.objects.filter(vendor=vendor).order_by('created_at')
    context = {
        'categories': categories,
    }
    return render(request, 'home/vendor/menu_builder.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def online_item_by_category(request, pk=None):
    vendor =  get_vendor(request)
    category = get_object_or_404(Category, pk=pk)
    onlineitem = OnlineItem.objects.filter(vendor=vendor, category=category)
    context = {
        'onlineitem': onlineitem,
        'category': category,                   
    }
    return render(request, 'home/vendor/online_item_by_category.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.vendor = get_vendor(request)
            category.slug = slugify(category_name)
            form.save()
            messages.success(request, 'Category added successfully.')
            return redirect('menu_builder')
    else:
        form = CategoryForm()
        # modify this form
        form.fields['category_name'].queryset = Category.objects.filter(vendor=get_vendor(request))
    context = {
        'form': form,
    }
    return render(request, 'home/vendor/add_category.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def edit_category(request, pk=None):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.vendor = get_vendor(request)
            category.slug = slugify(category_name)
            form.save()
            messages.success(request, 'Category updated successfully.')
            return redirect('menu_builder')
    else:
        form = CategoryForm(instance=category)
    context = {
        'form': form,
        'category': category,
    }
    return render(request, 'home/vendor/edit_category.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def delete_category(request, pk=None):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    messages.success(request, 'Category has been deleted successfully.')
    return redirect('menu_builder')


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def add_item(request):
    if request.method == 'POST':
        form = OnlineItemForm(request.POST, request.FILES)
        if form.is_valid():
            item_title = form.cleaned_data['item_title']
            item = form.save(commit=False)
            item.vendor = get_vendor(request)
            item.slug = slugify(item_title)
            form.save()
            messages.success(request, 'Online Item added successfully.')
            return redirect('online_item_by_category', item.category.id)
    else:
        form = OnlineItemForm()
    context = {
        'form': form,
    }
    return render(request, 'home/vendor/add_item.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def edit_item(request, pk=None):
    item = get_object_or_404(OnlineItem, pk=pk)
    if request.method == 'POST':
        form = OnlineItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            itemtitle = form.cleaned_data['item_title']
            item = form.save(commit=False)
            item.vendor = get_vendor(request)
            item.slug = slugify(itemtitle)
            form.save()
            messages.success(request, 'Online Item updated successfully.')
            return redirect('online_item_by_category', item.category.id)
    else:
        form = OnlineItemForm(instance=item)
        form.fields['category'].queryset = Category.objects.filter(vendor=get_vendor(request))
    context = {
        'form': form,
        'item': item,
    }
    return render(request, 'home/vendor/edit_item.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def delete_item(request, pk=None):
    item = get_object_or_404(OnlineItem, pk=pk)
    item.delete()
    messages.success(request, 'Online item has been deleted successfully.')
    return redirect('online_item_by_category', item.category.id)

