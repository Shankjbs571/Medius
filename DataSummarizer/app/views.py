from django.shortcuts import render
from .templates import *
import os
import pandas as pd
from django.http import HttpResponse


def home(request):
    return render( request, "home.html")

def upload_files(request):
    if request.method == 'POST' and request.FILES['file']:
        data = []
        uploaded_files = request.FILES.getlist('file')
        
        print(uploaded_files)
        for uploaded_file in uploaded_files:
            file_extension = os.path.splitext(uploaded_file.name)[1].lower()
            if file_extension == '.xlsx':
                df = pd.read_excel(uploaded_file)
                dpd_counts = df.groupby(['Cust State', 'DPD']).size().reset_index(name='Count')
                dpd_counts.to_excel('Summary.xlsx', index=False, sheet_name='Sheet1')
            elif file_extension == '.csv':
                df = pd.read_csv(uploaded_file)
                dpd_counts = df.groupby(['Cust State', 'DPD']).size().reset_index(name='Count')
                dpd_counts.to_excel('Summary.xlsx', index=False, sheet_name='Sheet1')

        output_path = 'Summary.xlsx'
        df.to_excel(output_path, index=False)

        # Serve the Excel file as a download
        with open(output_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=Summary.xlsx'
            return response
    return render(request, 'your_template.html')


def dpd_counts(file):
    df = pd.read_csv(file)
    dpd_counts = df.groupby(['Cust State', 'DPD']).size().reset_index(name='Count')
    Summary = dpd_counts.to_excel('Summary.xlsx', index=False, sheet_name='Sheet1')
    return Summary
