from django.shortcuts import render
import plotly.express as px
import plotly.graph_objects as go
from entries.models import Entry
from cars.models import Car
from django.contrib.auth.decorators import login_required
import pandas as pd
from django.db.models.functions import TruncMonth
from django.db.models import Count
from datetime import datetime, timedelta


@login_required
def render_graphs(request, car_id):
    """
        Views rendering page with graphs representing car exploitation data
    """
    try:
        car = Car.objects.get(user=request.user, id=car_id)
    except Car.DoesNotExist:
        print('message')

    this_car_entries = Entry.objects.filter(car=car).order_by('-date')
    other_cars_entries = Entry.objects.filter(car__make=car.make, car__model=car.model).order_by('-date')

    if len(this_car_entries) < 1:
        context = {'no_data': True}
    else:
        context = {
            'mileage_graph': create_mileage_graph(this_car_entries=this_car_entries, car=car),
            'costs_graph': create_costs_graph(entries=this_car_entries, car=car),
        }

    return render(
        request=request,
        template_name='graphs.html',
        context=context,
    )


def create_costs_graph(entries: list[Entry], car: Car) -> str:
    """
        Function creating costs by month graph
    """
    queryset = entries.values('date', 'cost').order_by('date')
    data = [{list(dict.values())[0].strftime('%m/%Y'): list(dict.values())[1]} for dict in queryset]

    grouped_data = {}
    for dict in data:
        for key, value in dict.items():
            grouped_data.setdefault(key, 0)
            grouped_data[key] += value

    first_date_key = list(grouped_data.keys())[0].split('/')
    start_date = datetime(int(first_date_key[1]), int(first_date_key[0]), 1)

    current_date = datetime.now()
    date_list = []
    while start_date <= current_date:
        date_list.append(start_date.strftime('%m/%Y'))
        start_date = start_date.replace(day=1)
        start_date = start_date + timedelta(days=32)
        start_date = start_date.replace(day=1)

    filled_expenses_list = {date: grouped_data[date] if date in grouped_data.keys() else 0 for date in date_list}
    df = pd.DataFrame({
        'month': filled_expenses_list.keys(),
        'expenses': filled_expenses_list.values(),
    })

    fig = px.bar(df, x='month', y='expenses').update_xaxes(type='category', title='Months').update_yaxes(title='Expenses [zł]')
    return fig.to_html()


def create_mileage_graph(this_car_entries: list[Entry], car: Car) -> str:
    """
        Function creating mileage across exploitation period graph
    """
    mileage_df = pd.DataFrame({
        'date': this_car_entries.values_list('date', flat=True),
        'mileage': this_car_entries.values_list('mileage', flat=True),
    })

    fig = go.Figure().add_trace(go.Scatter(x=mileage_df['date'], y=mileage_df['mileage'], mode='lines', name=f'Your {car.make} {car.model}'))
    fig.update_layout(title='Car mileage:', xaxis_title='Date', yaxis_title='Mileage [km]')
    return fig.to_html()





def foo(this_car_entries: list[Entry], other_cars_entries: list[Entry], car: Car) -> str:
    """
        Function creating mileage across exploitation period graph
    """
    mileage_df = pd.DataFrame({
        'date': this_car_entries.values_list('date', flat=True),
        'mileage': this_car_entries.values_list('mileage', flat=True),
    })

    other_cars_mileage_df = pd.DataFrame({
        'date': this_car_entries.values_list('date', flat=True),
        'mileage': other_cars_entries.values_list('mileage', flat=True),
    })

    fig = go.Figure().add_trace(go.Scatter(x=mileage_df['date'], y=mileage_df['mileage'], mode='lines', name=f'Your {car.make} {car.model}'))
    fig.add_trace(go.Scatter(x=other_cars_mileage_df['date'], y=other_cars_mileage_df['mileage'], mode='lines', name=f'Average for {car.make} {car.model}'))
    fig.update_layout(title='Car mileage:', xaxis_title='Date', yaxis_title='Mileage [km]')
    return fig.to_html()
