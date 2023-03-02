from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Sum, Count, IntegerField
from django.db.models.functions import TruncDay
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.utils.timezone import make_aware
# Prepare PDF data
from io import BytesIO
from datetime import datetime
   
import csv



from hotelbar.models import *
from hotelbar.forms import *

def sales_report(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date and end_date:
        start_date = make_aware(datetime.strptime(start_date, '%Y-%m-%d'))
        end_date = make_aware(datetime.strptime(end_date, '%Y-%m-%d'))
        sales_records = SalesRecord.objects.filter(sale_time__range=[start_date, end_date])
    else:
        sales_records = SalesRecord.objects.all()

    total_sales = sales_records.aggregate(Sum('total_price'))['total_price__sum'] or 0
    total_items_sold = sales_records.aggregate(Count('item'))['item__count'] or 0
    sales_by_item = sales_records.values('item__name').annotate(total_sales=Sum('total_price')).order_by('-total_sales')
    sales_by_day = sales_records.annotate(day=TruncDay('sale_time')).values('day').annotate(total_sales=Sum('total_price')).order_by('-day')

    context = {
        'start_date': start_date,
        'end_date': end_date,
        'total_sales': total_sales,
        'total_items_sold': total_items_sold,
        'sales_by_item': sales_by_item,
        'sales_by_day': sales_by_day,
    }

    if request.GET.get('export') == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="sales_summary_report.csv"'
        writer = csv.writer(response)
        writer.writerow(['Start Date', 'End Date', 'Total Sales', 'Total Items Sold'])
        writer.writerow([start_date, end_date, total_sales, total_items_sold])
        writer.writerow([])
        writer.writerow(['Sales by Item'])
        writer.writerow(['Item Name', 'Total Sales'])
        for item in sales_by_item:
            writer.writerow([item['item__name'], item['total_sales']])
        writer.writerow([])
        writer.writerow(['Sales by Day'])
        writer.writerow(['Day', 'Total Sales'])
        for day in sales_by_day:
            writer.writerow([day['day'], day['total_sales']])
        return response

    if request.GET.get('export') == 'pdf':
        template = get_template('sales_summary_report_pdf.html')
        context = {
            'start_date': start_date,
            'end_date': end_date,
            'total_sales': total_sales,
            'total_items_sold': total_items_sold,
            'sales_by_item': sales_by_item,
            'sales_by_day': sales_by_day,
        }
        html = template.render(context)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="sales_summary_report_{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}.pdf"'
        pisa.CreatePDF(html, dest=response)
        return response

    return render(request, 'sales_summary_report.html', context)


# def sales_report(request):
#     sales = SalesRecord.objects.all()

#     # Get total sales and total number of items sold
#     total_sales = sales.aggregate(total_sales=Sum('total_price'))['total_sales'] or 0
#     total_items_sold = sales.aggregate(total_items_sold=Sum('quantity'))['total_items_sold'] or 0

#     # Get sales by item
#     sales_by_item = sales.values('item__name').annotate(total_sales=Sum('total_price'), total_items_sold=Sum('quantity')).order_by('-total_sales')

#     # Get sales by day
#     sales_by_day = sales.annotate(day=TruncDay('sale_time')).values('day').annotate(total_sales=Sum('total_price'), total_items_sold=Sum('quantity')).order_by('-day')

#     # Prepare CSV data
#     csv_data = []
#     csv_data.append(['Total Sales', 'Total Items Sold'])
#     csv_data.append([total_sales, total_items_sold])
#     csv_data.append([])  # Blank row
#     csv_data.append(['Sales by Item'])
#     csv_data.append(['Item Name', 'Total Sales', 'Total Items Sold'])
#     for item in sales_by_item:
#         csv_data.append([item['item__name'], item['total_sales'], item['total_items_sold']])
#     csv_data.append([])  # Blank row
#     csv_data.append(['Sales by Day'])
#     csv_data.append(['Date', 'Total Sales', 'Total Items Sold'])
#     for day in sales_by_day:
#         csv_data.append([day['day'].strftime('%Y-%m-%d'), day['total_sales'], day['total_items_sold']])

#     response = HttpResponse(content_type='text/csv')
#     response['Content-Disposition'] = f'attachment; filename="sales_report_{datetime.now().strftime("%Y-%m-%d_%H:%M:%S")}.csv"'
#     writer = csv.writer(response)
#     for row in csv_data:
#         writer.writerow(row)

    

#     pdf_data = BytesIO()
#     template = get_template('sales_summary_report_pdf.html')
#     context = {
#         'total_sales': total_sales,
#         'total_items_sold': total_items_sold,
#         'sales_by_item': sales_by_item,
#         'sales_by_day': sales_by_day,
#     }
#     html = template.render(context)
#     pisa.CreatePDF(BytesIO(html.encode('utf-8')), pdf_data)

#     # Set the appropriate PDF response headers
#     response_pdf = HttpResponse(pdf_data.getvalue(), content_type='application/pdf')
#     response_pdf['Content-Disposition'] = f'attachment; filename="sales_report_{datetime.now().strftime("%Y-%m-%d_%H:%M:%S")}.pdf"'

#     if request.GET.get('export') == 'pdf':
#         return response_pdf
#     else:
#         return response
















@login_required
def sales_list(request):
    sales_records = SalesRecord.objects.all()
    return render(request, 'sales/sales_list.html', {'sales_records': sales_records,  'section': 'sales'})

@login_required
def sales_detail(request, pk):
    sales_record = get_object_or_404(SalesRecord, pk=pk)
    return render(request, 'sales/sales_detail.html', {'sales_record': sales_record})


@login_required
def sales_add(request):
    if request.method == 'POST':
        form = SalesRecordForm(request.POST)
        if form.is_valid():
            sales_record = form.save(commit=False)
            sales_record.sold_by_id = request.user.id
            sales_record.save()
            messages.success(request, 'Sale recorded.')
            return redirect('sales_list')
    else:
        form = SalesRecordForm()
    return render(request, 'sales/sales_add.html', {'form': form})


@login_required
def sales_edit(request, pk):
    sale = get_object_or_404(SalesRecord, pk=pk)
    if request.method == 'POST':
        form = SalesRecordForm(request.POST, instance=sale)
        if form.is_valid():
            sale = form.save(commit=False)
            sale.sold_by = request.user
            sale.save()
            messages.success(request, 'Sale updated successfully')
            return redirect('sales_list')
    else:
        form = SalesRecordForm(instance=sale)
    return render(request, 'sales/sales_edit.html', {'form': form, 'sale': sale})


@login_required
def sales_delete(request, pk):
    sales_record = get_object_or_404(SalesRecord, pk=pk)
    if request.method == 'POST':
        sales_record.delete()
        messages.success(request, 'Sales record deleted.')
        return redirect('sales_list')
    return render(request, 'sales/sales_delete.html', {'sales_record': sales_record})


# @login_required
# def sales_record_list(request):
#     sales_records = SalesRecord.objects.all()
#     return render(request, 'sales_record_list.html', {'sales_records': sales_records})

# @login_required
# def sales_record_detail(request, pk):
#     sales_record = get_object_or_404(SalesRecord, pk=pk)
#     return render(request, 'sales_record_detail.html', {'sales_record': sales_record})

# @login_required
# def sales_record_create(request):
#     if request.method == 'POST':
#         form = SalesRecordForm(request.POST)
#         if form.is_valid():
#             sales_record = form.save(commit=False)
#             sales_record.sold_by = request.user
#             sales_record.save()
#             messages.success(request, 'Sales record created successfully!')
#             return redirect('sales_record_detail', pk=sales_record.pk)
#     else:
#         form = SalesRecordForm()
#     return render(request, 'sales_record_form.html', {'form': form})

# @login_required
# def sales_record_update(request, pk):
#     sales_record = get_object_or_404(SalesRecord, pk=pk)
#     if request.method == 'POST':
#         form = SalesRecordForm(request.POST, instance=sales_record)
#         if form.is_valid():
#             sales_record = form.save()
#             messages.success(request, 'Sales record updated successfully!')
#             return redirect('sales_record_detail', pk=sales_record.pk)
#     else:
#         form = SalesRecordForm(instance=sales_record)
#     return render(request, 'sales_record_form.html', {'form': form})

# @login_required
# def sales_record_delete(request, pk):
#     sales_record = get_object_or_404(SalesRecord, pk=pk)
#     sales_record.delete()
#     messages.success(request, 'Sales record deleted successfully!')
#     return redirect('sales_record_list')

