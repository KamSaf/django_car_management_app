from cars.models import Car
from django.contrib.auth.models import User


def get_viewed_car(user: User, car_id: int = None) -> Car | None:
    """
        Get Car object to display on the home page
    """
    viewed_car = None
    cars = Car.objects.filter(user=user).all()
    if car_id:
        viewed_car = cars.filter(id=car_id).first()

    if not viewed_car:
        try:
            viewed_car = cars.get(favourite=True)
        except Car.DoesNotExist:
            viewed_car = cars[0]

    return viewed_car
