from django.shortcuts import render, redirect
import plotly.express as px
import plotly.graph_objects as go
from entries.models import Entry
from cars.models import Car
from django.contrib.auth.decorators import login_required
import pandas as pd
from datetime import datetime, timedelta
from django.contrib import messages


@login_required
def render_graphs(request, car_id, graph):
    """
        Views rendering page with graphs representing car exploitation data
    """
    try:
        car = Car.objects.get(user=request.user, id=car_id)
    except Car.DoesNotExist:
        messages.error(request, 'This car does not exist.')
        return redirect(to="home_page")

    this_car_entries = Entry.objects.filter(car=car).order_by('-date')
    other_cars_entries = Entry.objects.filter(car__make=car.make, car__model=car.model).order_by('-date')

    if len(this_car_entries) < 1:
        return render(request=request, template_name='graphs.html', context={'no_data': True})

    match(graph):
        case 'mileage':
            graph_html = mileage_graph(this_car_entries=this_car_entries, car=car)
        case 'expenses':
            graph_html = costs_graph(entries=this_car_entries, car=car)
        case 'costs_to_mileage':
            graph_html = service_costs_graph(entries=this_car_entries, car=car)
        case 'fuel_economy':
            graph_html = None
    return render(
        request=request,
        template_name='graphs.html',
        context={
            'graph': graph_html,
            'car': car,
            'graph_name': graph,
        },
    )


def costs_graph(entries: list[Entry], car: Car) -> str:
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
    fig.update_layout(autosize=True)
    return fig.to_html()


def mileage_graph(this_car_entries: list[Entry], car: Car) -> str:
    """
        Function creating mileage across exploitation period graph
    """
    mileage_df = pd.DataFrame({
        'date': this_car_entries.values_list('date', flat=True),
        'mileage': this_car_entries.values_list('mileage', flat=True),
    })

    fig = go.Figure().add_trace(go.Scatter(x=mileage_df['date'], y=mileage_df['mileage'], mode='lines', name=f'Your {car.make} {car.model}'))
    fig.update_layout(autosize=True, title='Car mileage:', xaxis_title='Date', yaxis_title='Mileage [km]', )
    return fig.to_html()


def service_costs_graph(entries: list[Entry], car: Car) -> str:
    """
        Function creating service costs to mileage graph
    """
    queryset = entries.filter(category='service').values('mileage', 'cost').order_by('date')

    data = [{list(dict.values())[0]: list(dict.values())[1]} for dict in queryset]

    costs = [list(dict.values())[0] for dict in data]

    for i in range(len(costs)):
        if i > 0:
            costs[i] += costs[i - 1]

    this_car_df = pd.DataFrame({
        'costs': costs,
        'mileage': [list(dict.keys())[0] for dict in data],
    })

    fig = go.Figure().add_trace(go.Scatter(x=this_car_df['mileage'], y=this_car_df['costs'], mode='lines', name=f'Your {car.make} {car.model}'))
    fig.update_layout(autosize=True, title='Car mileage to service costs:', xaxis_title='Mileage [km]', yaxis_title='Expenses')
    return fig.to_html()


def fuel_economy_graph(this_car_entries: list[Entry], other_cars_entries: list[Entry], car: Car) -> str:
    """
        Function creating fuel economy across exploitation period graph
    """
    mileage_df = pd.DataFrame({
        'date': this_car_entries.values_list('date', flat=True),
        'mileage': this_car_entries.values_list('mileage', flat=True),
    })

    fig = go.Figure().add_trace(go.Scatter(x=mileage_df['date'], y=mileage_df['mileage'], mode='lines', name=f'Your {car.make} {car.model}'))
    fig.update_layout(autosize=True, title='Car mileage:', xaxis_title='Date', yaxis_title='Mileage [km]', )
    return fig.to_html()
