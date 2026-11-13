"""Views for starting and ending a session: logging in and logging out."""

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from allocations.forms import LogInForm
from allocations.forms import CSVUploadForm

# for csv upload
import csv
import io
import random



def home(request):
    """Show the home page, or the dashboard if the user is logged in."""
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'home.html')


def log_in(request):
    """Show the log in form and log the user in."""
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = LogInForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('dashboard')
    else:
        form = LogInForm(request)
    return render(request, 'log_in.html', {'form': form})


@require_POST
def log_out(request):
    """Log the user out. Only POST requests are allowed (see base.html)."""
    logout(request)
    return redirect('home')


@login_required
def dashboard(request):
    """Show the page users see after logging in."""
    return render(request, 'dashboard.html')


def read_csv(uploaded_file):
    """
    text = uploaded_file.read().decode('utf-8-sig')
    rows = list(csv.reader(io.StringIO(text)))
    if not rows:
        return [], []
    return rows[0], rows[1:]
    """

    """Return the CSV rows as a list of dicts, keyed by the header row."""
    text = uploaded_file.read().decode('utf-8-sig')
    return list(csv.DictReader(io.StringIO(text)))


@login_required
def import_csv(request):
    """
    form = CSVUploadForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        header, rows = read_csv(form.cleaned_data['csv_file'])
        return render(request, 'csv_report.html',
            {'header': header, 'rows': rows, 'form':form})
    return render(request, 'import_csv.html', {'form': form})
    """
    form = CSVUploadForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        students = read_csv(form.cleaned_data['csv_file'])
        headers = list(students[0].keys()) if students else []
        return render(request, 'csv_report.html',
            {'students': students, 'headers': headers, 'form': form})
    return render(request, 'import_csv.html', {'form': form})


