from django.contrib import admin
from django.urls import path, include, re_path
import uuid
from . import views

urlpatterns = [
    re_path(r'^index/$', views.index, name="index"),
    re_path(r'^$', views.dashboard, name="dashboard"),

    # mannufacturer
    re_path(r'^manufacturer/manufacturers/$', views.manufacturers, name="manufacturers"),
    re_path(r'^manufacturer/remove-manufacturer-item/(?P<pk>\d+)/$', views.remove_manufacturer, name="remove_manufacturer"),
    re_path(r'^manufacturer/add-manufacturer/$', views.add_manufacturer, name="add_manufacturer"),
    re_path(r'^manufacturer/edit-manufacturer/(?P<pk>\d+)/$', views.edit_manufacturer, name="edit_manufacturer"),

    # medicine section
    re_path(r'^medicine/add-new-medicine/$', views.add_new_medicine, name="add_new_medicine"),
    re_path(r'^medicine/mark-as-expired/(?P<pk>\d+)/$', views.mark_as_expired, name="mark_as_expired"),
    re_path(r'^medicine/remove-medicine-item/(?P<pk>\d+)/$', views.remove_medicine_item, name="remove_medicine_item"),
    re_path(r'^medicine/edit-medicine-item/(?P<pk>\d+)/$', views.edit_medicine_item, name="edit_medicine_item"),
    re_path(r'^medicine/active-medicine-list/$', views.active_medicine_list, name="active_medicine_list"),
    re_path(r'^medicine/expired-medicine-list/$', views.expired_medicine_list, name="expired_medicine_list"),

    # order section
    re_path(r'^order/active-order/$', views.active_orders, name="active_orders"),
    re_path(r'^order/cancelled-order/$', views.cancelled_orders, name="cancelled_orders"),
    re_path(r'^order/delivered-order/$', views.delivered_orders, name="delivered_orders"),
    re_path(r'^order/marked-as-delivered-cancelled-active/(?P<pk>\d+)/(?P<mark_status>\w+)/$', views.mark_as_delivered_or_cancelled_or_active, name="mark_as_delivered_or_cancelled_or_active"),

    # invoices
    re_path(r'^invoices/(?P<pk>\d+)/$', views.invoice, name="invoice"),

    re_path(r'^my-profile/$', views.profile, name="profile"),
    re_path(r'^login-user/$', views.login_view, name="login_view"),
    re_path(r'^register-user/$', views.register_view, name="register_view"),

]