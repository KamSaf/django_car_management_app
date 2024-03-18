from cars.models import Car
from entries.models import Entry
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


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
        Function creating costs by month graph
    """
    fuel_queryset = this_car_entries.filter(category='fuel').values('date', 'fuel_liters').order_by('date')
    mileage_queryset = this_car_entries.values('date', 'mileage').order_by('date')

    if len(fuel_queryset) > 1 and len(mileage_queryset) > 1:
        data_fuel = [{list(dict.values())[0].strftime('%m/%Y'): list(dict.values())[1]} for dict in fuel_queryset]
        data_mileage = [{list(mileage_queryset[i].values())[0].strftime('%m/%Y'): (list(mileage_queryset[i].values())[1] - list(mileage_queryset[i - 1].values())[1])} for i in range(1, len(mileage_queryset))]

        grouped_data_fuel = {}
        for dict in data_fuel:
            for key, value in dict.items():
                grouped_data_fuel.setdefault(key, 0)
                grouped_data_fuel[key] += value

        grouped_data_mileage = {}
        for dict in data_mileage:
            for key, value in dict.items():
                grouped_data_mileage.setdefault(key, 0)
                grouped_data_mileage[key] += value

        data = {}
        for date, mileage in grouped_data_mileage.items():
            data[date] = (grouped_data_fuel[date] * 100) / mileage if date in grouped_data_fuel.keys() else 0

        df = pd.DataFrame({
            'month': data.keys(),
            'expenses': data.values(),
        })

        fig = go.Figure().add_trace(go.Scatter(x=df['month'], y=df['expenses'], mode='lines', name=f'Your {car.make} {car.model}'))
        fig.update_layout(autosize=True, title='Fuel economy:', xaxis_title='Month', yaxis_title='Fuel [l/km]', )
        return fig.to_html()