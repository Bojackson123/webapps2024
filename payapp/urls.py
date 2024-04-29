from django.urls import path
from . import views

urlpatterns = [
    path("", views.view_transactions, name="view_transactions"),
    path("change_currency/", views.change_currency, name="change_currency"),
    path("send_payment/", views.send_payment, name="send_payment"),
    path("request_payment/", views.request_payment, name="request_payment"),
    path("accept-payment-request/<int:request_id>/",
         views.accept_payment_request,
         name="accept_payment_request",
         ),
    path("reject-payment-request/<int:request_id>/",
         views.reject_payment_request,
         name="reject_payment_request",
         ),
    path("users_transactions/", views.users_transactions, name="users_transactions"),
    path("change-admin-status/",
         views.change_admin_status,
         name="admin_status_change_url",
         ),
    path("create_admin/",
         views.create_admin,
         name="create_admin",
         ),
]
