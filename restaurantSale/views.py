import datetime

from django.db.models import Sum
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from datetime import timedelta
from django.db import models

from .models import Restaurantsale
from .forms import RestaurantsaleForm


def restaurant_sale_report(request):
    # Set default date range to today
    today = timezone.now().date()
    date_from_str = request.GET.get('date_from', today.strftime('%Y-%m-%d'))
    date_to_str = request.GET.get('date_to', today.strftime('%Y-%m-%d'))

    # Convert date strings to date objects
    try:
        date_from = datetime.datetime.strptime(date_from_str, '%Y-%m-%d').date()
    except (TypeError, ValueError):
        date_from = today
    try:
        date_to = datetime.datetime.strptime(date_to_str, '%Y-%m-%d').date()
    except (TypeError, ValueError):
        date_to = today

    # Filter sales by date range
    sales = Restaurantsale.objects.filter(date__range=[date_from, date_to]).annotate(total_price=models.F('number_of_plates') * models.F('price'))

    # Calculate total sales for the selected date range
    total_sales = sales.aggregate(Sum('total_price'))['total_price__sum'] or 0

    # Get total sales for each mode of payment
    pos_sales = sales.filter(payment_mode='POS').aggregate(Sum('total_price'))['total_price__sum'] or 0
    transfer_sales = sales.filter(payment_mode='TRANSFER').aggregate(Sum('total_price'))['total_price__sum'] or 0
    cash_sales = sales.filter(payment_mode='CASH').aggregate(Sum('total_price'))['total_price__sum'] or 0
    debt_sales = sales.filter(payment_mode='DEBT').aggregate(Sum('total_price'))['total_price__sum'] or 0
    complimentary_sales = sales.filter(payment_mode='COMPLIMENTARY').aggregate(Sum('total_price'))['total_price__sum'] or 0

    context = {
        'sales': sales,
        'total_sales': total_sales,
        'date_from': date_from,
        'date_to': date_to,
        'pos_sales': pos_sales,
        'transfer_sales': transfer_sales,
        'cash_sales': cash_sales,
        'debt_sales': debt_sales,
        'complimentary_sales': complimentary_sales,
        'section': 'restaurant_sale_report'
    }

    return render(request, 'restaurant_sale_report.html', context)
def sale_list(request):
    sales = Restaurantsale.objects.all()
    for sale in sales:
        sale.total = sale.total_price()
    return render(request, 'sale_list.html', {'sales': sales})

def new_sale(request):
    if request.method == 'POST':
        form = RestaurantsaleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sale_list')
    else:
        form = RestaurantsaleForm()
    choices = Restaurantsale.MODE_OF_PAYMENT_CHOICES # pass the choices to the context
    context = {
        'form': form,
        'choices': choices,
    }
    return render(request, 'new_sale.html', context)

def sale_detail(request, pk):
    sale = get_object_or_404(Restaurantsale, pk=pk)
    return render(request, 'sale_detail.html', {'sale': sale})

def sale_update(request, pk):
    sale = get_object_or_404(Restaurantsale, pk=pk)
    if request.method == 'POST':
        form = RestaurantsaleForm(request.POST, instance=sale)
        if form.is_valid():
            form.save()
            return redirect('sale_detail', pk=sale.pk)
    else:
        form = RestaurantsaleForm(instance=sale)
    return render(request, 'sale_update.html', {'form': form})
