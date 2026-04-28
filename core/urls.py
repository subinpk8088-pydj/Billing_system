from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

def home_redirect(request):
    return redirect('/billing/invoices/')

urlpatterns = [
    path('', home_redirect),  # ✅ FIX
    path('admin/', admin.site.urls),
    path('billing/', include('billing.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]