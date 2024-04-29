from django.shortcuts import render, redirect
from django.contrib import messages
import json
from .models import Transaction
import requests
from django.db import transaction as db_transaction
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from django.contrib.auth import get_user_model
from django.contrib.admin.views.decorators import staff_member_required
from .forms import CurrencyForm
from django.urls import reverse

User = get_user_model()

@login_required(login_url='/webapps2024/login/')
def send_payment(request):
    if request.method == "POST":
        receiver_identifier = request.POST.get("receiver")
        amount = Decimal(request.POST.get("amount"))
        converted_amount = amount
        try:
            receiver = (
                User.objects.filter(email=receiver_identifier).first()
                or User.objects.filter(username=receiver_identifier).first()
            )

            if amount <= 0:
                raise ValueError("Amount must be positive")

            if receiver is None:
                raise ValueError("User not found")

            if request.user.balance < amount:
                raise ValueError("Insufficient balance")

            if receiver == request.user:
                raise ValueError("You cannot send money to yourself")

            if receiver and request.user.balance >= amount and amount > 0:
                with db_transaction.atomic():
                    request.user.balance -= amount
                    if not receiver.currency == request.user.currency:
                        # HTTP call to convert currency
                        url = request.build_absolute_uri(
                            reverse('convert_currency', kwargs={
                                'currency1': request.user.currency, 'currency2': receiver.currency,
                                'amount_of_currency1': amount
                            })
                        )
                        response = requests.get(url)
                        data = response.json()
                        amount = Decimal(data["converted_amount"])

                    receiver.balance += amount
                    Transaction.objects.create(
                        sender=request.user, receiver=receiver,
                        amount=amount, converted_amount=converted_amount,
                        currency_sign=request.user.currency
                    )
                    request.user.save()
                    receiver.save()

                messages.success(request, "Transaction completed successfully.")
                return redirect(
                    "send_payment"
                )

        except ValueError as e:
            messages.error(request, str(e))

    return render(request, "send_payment.html")


@login_required(login_url='/webapps2024/login/')
def request_payment(request):
    if request.method == "POST":
        receiver_identifier = request.POST.get("receiver")
        amount = Decimal(request.POST.get("amount"))
        converted_amount = amount

        receiver = (
            User.objects.filter(username=receiver_identifier).first()
            or User.objects.filter(email=receiver_identifier).first()
        )

        if receiver and amount > 0 and receiver != request.user:

            if not receiver.currency == request.user.currency:
                url = request.build_absolute_uri(
                    reverse('convert_currency', kwargs={
                        'currency1': request.user.currency, 'currency2': receiver.currency,
                        'amount_of_currency1': amount
                    })
                )
                response = requests.get(url)
                data = response.json()
                converted_amount = Decimal(data["converted_amount"])
            tr = Transaction.objects.create(
                sender=receiver, receiver=request.user, amount=amount,
                converted_amount=converted_amount, currency_sign=receiver.currency,
                is_request=True
            )
            tr.save()
            messages.success(request, "Payment request sent successfully.")
            return redirect("request_payment")
        else:
            messages.error(request, "Invalid receiver or amount.")

    return render(request, "request_payment.html")


from django.db.models import Q


@login_required(login_url='/webapps2024/login/')
def view_transactions(request):
    current_tab = request.GET.get("tab", "sent_payments")
    re_transactions = Transaction.objects.filter(
        Q(receiver=request.user, is_request=False)
        | Q(receiver=request.user, is_convert=True)
    ).order_by("-timestamp")
    sent_transactions = Transaction.objects.filter(
        Q(sender=request.user, is_request=False)
        | Q(sender=request.user, is_convert=True)
    ).order_by("-timestamp")
    sent_request_transactions = Transaction.objects.filter(
        receiver=request.user, is_request=True
    ).order_by("-timestamp")
    re_request_transactions = Transaction.objects.filter(
        sender=request.user, is_request=True
    ).order_by("-timestamp")
    return render(
        request,
        "transactions.html",
        {
            "re_transactions": re_transactions,
            "sent_transactions": sent_transactions,
            "sent_request_transactions": sent_request_transactions,
            "re_request_transactions": re_request_transactions,
            "current_tab": current_tab,
        },
    )


@staff_member_required
@login_required(login_url='/webapps2024/login/')
def users_transactions(request):
    current_tab = request.GET.get("tab", "transactions")
    transactions = Transaction.objects.all().order_by("-timestamp")
    all_users = User.objects.all()
    return render(
        request,
        "users_transactions.html",
        {
            "transactions": transactions,
            "all_users": all_users,
            "current_tab": current_tab,
        },
    )


@login_required(login_url='/webapps2024/login/')
def accept_payment_request(request, request_id):
    transaction = Transaction.objects.filter(
        id=request_id, sender=request.user, is_request=True
    ).first()
    if transaction:
        with db_transaction.atomic():
            request.user.balance -= transaction.converted_amount
            transaction.receiver.balance += transaction.amount
            transaction.is_accepted = True
            transaction.is_convert = True
            request.user.save()
            transaction.receiver.save()
            transaction.save()
            messages.success(request, "Payment request accepted successfully.")
    else:
        messages.error(request, "Invalid transaction ID.")

    url = reverse("view_transactions") + "?tab=re_request_payments"
    return redirect(url)


@login_required(login_url='/webapps2024/login/')
def reject_payment_request(request, request_id):
    transaction = Transaction.objects.filter(
        id=request_id, sender=request.user, is_request=True
    ).first()
    if transaction:
        transaction.is_rejected = True
        transaction.save()
        messages.success(request, "Payment request rejected successfully.")
    else:
        messages.error(request, "Invalid transaction ID.")

    url = reverse("view_transactions") + "?tab=re_request_payments"
    return redirect(url)


@login_required(login_url='/webapps2024/login/')
def change_currency(request):
    if request.method == "POST":
        form = CurrencyForm(request.POST)
        if form.is_valid():
            user = User.objects.get(id=request.user.id)
            currency2 = form.cleaned_data.get('currency')
            currency1 = user.currency
            amount_of_currency1 = user.balance

            # Call to RESTServiceAPI
            url = request.build_absolute_uri(
                reverse('convert_currency', kwargs={
                    'currency1': currency1, 'currency2': currency2,
                    'amount_of_currency1': amount_of_currency1
                })
            )
            response = requests.get(url)
            data = response.json()
            user.balance = float(data["converted_amount"])
            user.currency = currency2
            user.save()
            messages.success(request, "Currency and balance updated successfully.")
            return redirect("change_currency")
    else:
        form = CurrencyForm(instance=request.user)

    return render(request, "change_currency.html", {"form": form})


@staff_member_required
@login_required(login_url='/webapps2024/login/')
def change_admin_status(request):
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        is_admin = request.POST.get("is_admin") == "on"

        try:
            user_to_update = User.objects.get(id=user_id)
            user_to_update.is_superuser = is_admin
            user_to_update.is_staff = is_admin

            user_to_update.save()

            messages.success(
                request, f"Admin status updated for {user_to_update.username}."
            )

        except User.DoesNotExist:
            messages.error(request, "User does not exist.")

    url = reverse("users_transactions") + "?tab=balance"
    return redirect(url)


@staff_member_required
@login_required(login_url='/webapps2024/login/')
def create_admin(request):
    url = reverse("users_transactions") + "?tab=create_user"

    if request.method == "POST":
        first_name = request.POST.get("first_name", None)
        last_name = request.POST.get("last_name", None)
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        try:

            if User.objects.filter(username=username).first():
                messages.error(request, "Username is taken.")
                return redirect(url)

            if User.objects.filter(email=email).first():
                messages.error(request, "Email is taken.")
                return redirect(url)

            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=username,
                password=password,
            )
            user.is_superuser = True
            user.is_staff = True
            user.save()

            messages.success(request, f"Super user {username} created successfully.")

        except Exception as e:
            messages.error(request, f"Error creating admin user: {e}")

    return redirect(url)
