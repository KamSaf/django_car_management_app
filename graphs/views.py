from django.shortcuts import render, redirect
from entries.models import Entry
from cars.models import Car
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .utils import service_costs_graph, costs_graph, fuel_economy_graph, mileage_graph

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
            # graph_html = fuel_economy_graph(this_car_entries=this_car_entries, other_cars_entries=other_cars_entries, car=car)
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
