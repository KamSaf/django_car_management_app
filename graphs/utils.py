from django.db.models import BaseManager
from cars.models import Car
from entries.models import Entry
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


def costs_graph(entries: BaseManager[Entry], car: Car) -> str:
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


def mileage_graph(this_car_entries: BaseManager[Entry], car: Car) -> str:
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


def fuel_economy_graph(this_car_entries: BaseManager[Entry], other_cars_entries: BaseManager[Entry], car: Car) -> str:
    """
        Function creating costs by month graph
    """
    fuel_queryset = this_car_entries.filter(category='fuel').values('date', 'fuel_liters').order_by('date')
    mileage_queryset = this_car_entries.values('date', 'mileage').order_by('date')

    this_car_df = fuel_cons(fuel_queryset=fuel_queryset, mileage_queryset=mileage_queryset)

    cars = other_cars_entries.distinct('car').values_list('car', flat=True)
    entries_by_cars = {}
    for car_id in cars:
        entries_by_cars[car_id] = (
            other_cars_entries.filter(car__id=car_id, category='fuel').values('date', 'fuel_liters').order_by('date'),
            other_cars_entries.filter(car__id=car_id).values('date', 'mileage').order_by('date')
        )

    avg_data = {month: 0 for month in this_car_df['month']}
    for value in entries_by_cars.values():
        df = fuel_cons(fuel_queryset=value[0], mileage_queryset=value[1], months_list=this_car_df['month'])
        for row in df.iterrows():
            avg_data[row[1].iloc[0]] += (row[1].iloc[1]) / len(entries_by_cars.values())

    avg_df = pd.DataFrame({
        'month': avg_data.keys(),
        'expenses': avg_data.values(),
    })

    fig = go.Figure().add_trace(go.Scatter(x=this_car_df['month'], y=this_car_df['expenses'], mode='lines', name=f'Your {car.make} {car.model}'))
    fig.add_trace(go.Scatter(x=avg_df['month'], y=avg_df['expenses'], mode='lines', name=f'Average for {car.make} {car.model}'))
    fig.update_layout(autosize=True, title='Fuel economy:', xaxis_title='Month', yaxis_title='Fuel [l/km]', )
    return fig.to_html()


def fuel_cons(fuel_queryset, mileage_queryset, months_list: list = None) -> pd.DataFrame:
    """
        Creates DataFrame with fuel consumption data for given fuel and mileage querysets of a car
    """
    if len(fuel_queryset) > 1 and len(mileage_queryset) > 1:
        data_fuel = [{list(dict.values())[0].strftime('%m/%Y'): list(dict.values())[1]} for dict in fuel_queryset]
        data_mileage = [{list(mileage_queryset[i].values())[0].strftime('%m/%Y'): (list(mileage_queryset[i].values())[1] - list(mileage_queryset[i - 1].values())[1])} for i in range(1, len(mileage_queryset))]

        grouped_data_fuel = group_data(data=data_fuel)
        grouped_data_mileage = group_data(data=data_mileage)

        data = {}
        for date, mileage in grouped_data_mileage.items():
            data[date] = (grouped_data_fuel[date] * 100) / mileage if date in grouped_data_fuel.keys() else 0

    this_car_df = pd.DataFrame({
        'month': data.keys() if data else [],
        'expenses': data.values() if data else [],
    })

    if months_list is not None:
        this_car_df = this_car_df[this_car_df['month'].isin(months_list)]
    return this_car_df


def group_data(data: list[dict]) -> dict:
    """
        Groups list of dictionaries into single dictionary
    """
    grouped_data = {}
    for dict in data:
        for key, value in dict.items():
            grouped_data.setdefault(key, 0)
            grouped_data[key] += value
    return grouped_data
