# from django.shortcuts import render
# from . forms import ProductForm,RequestViewForm,RegisterViewModel
# from django.core.mail import send_mail
# from django.conf import settings
# from django.contrib import messages

# def welcomepage(request):
#     return render(request,"welcomepage.html")

# def register_view(request):
#     if request.method == "POST":
#         form = RequestViewForm(request.POST)
#         if form.is_valid():
#             user =form.save()
#             fullname = form.cleaned_data["supplyername"]
#             email = form.cleaned_data["email"]
#             print("successfully saved..")

# # EMAIL PART
#             subject = "Registration Successfull"

#             message = f"""
#                         hello{fullname}, your registration has sucessfully completed

#                         Thank You !
#                     """
#             send_mail(subject,message,settings.DEFAULT_FROM_EMAIL,[email],fail_silently=False)
#             messages.success(request,"Registration successfull")
#     else:
#         form=RequestViewForm() 
#     return render(request,"register_view.html",{"form":form})


import logging

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.db.models import Avg, Count
from django.shortcuts import redirect, render

from .forms import QuoteRequestForm, ReviewForm, SupplierRegisterForm
from .models import Review

logger = logging.getLogger(__name__)


def _send_email(subject, message, recipient):
    """Email must never break a successful save, so errors are only logged."""
    try:
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [recipient], fail_silently=False)
    except Exception:
        logger.exception("Could not send email to %s", recipient)


def welcomepage(request):
    return render(request, "welcomepage.html")


def supplier_register(request):
    if request.method == "POST":
        form = SupplierRegisterForm(request.POST)
        if form.is_valid():
            supplier = form.save()
            _send_email(
                "Registration successful - Future Marketing",
                f"Hello {supplier.fullname},\n\nYour supplier registration with Future Marketing "
                "has been completed successfully.\n\nThank you!",
                supplier.email,
            )
            messages.success(request, "Registration successful! We have emailed you a confirmation.")
            return redirect("supplier_register")  # redirect after POST: no duplicate on refresh
    else:
        form = SupplierRegisterForm()
    return render(request, "supplier_register.html", {"form": form})


def reviews(request):
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you! Your review has been posted.")
            return redirect("reviews")
    else:
        form = ReviewForm()

    approved = Review.objects.filter(approved=True)
    summary = approved.aggregate(avg=Avg("rating"), total=Count("id"))
    total = summary["total"]
    avg = summary["avg"] or 0

    counts = dict(approved.order_by().values_list("rating").annotate(c=Count("id")))
    distribution = [
        {
            "star": s,
            "count": counts.get(s, 0),
            "pct": round(counts.get(s, 0) * 100 / total) if total else 0,
        }
        for s in range(5, 0, -1)
    ]

    page = Paginator(approved, 6).get_page(request.GET.get("page"))
    context = {
        "form": form,
        "page": page,
        "total": total,
        "avg": avg,
        "avg_stars": "★" * round(avg) + "☆" * (5 - round(avg)),
        "distribution": distribution,
    }
    return render(request, "reviews.html", context)


def request_quote(request):
    if request.method == "POST":
        form = QuoteRequestForm(request.POST)
        if form.is_valid():
            quote = form.save()
            _send_email(
                "We received your quote request - Future Marketing",
                f"Hello {quote.name},\n\nThanks for contacting Future Marketing. "
                "Our team will get back to you within one business day.",
                quote.email,
            )
            messages.success(request, "Quote request sent! We will reply within one business day.")
            return redirect("request_quote")
    else:
        form = QuoteRequestForm()
    return render(request, "request_quote.html", {"form": form})