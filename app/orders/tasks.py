import datetime
import pytz
from motochas.celery import app
from utilities.mapping import find_near_cron
from .models import OrderChecking, Order
from renter.models import Profile, RenterProduct
import requests


@app.task
def move_renter():
    try:
        today = datetime.datetime.today().date()
        order_checkings = OrderChecking.objects.filter(checking_start__date=today)
        for checking in order_checkings:
            difference_t = (
                        datetime.datetime.now(tz=pytz.timezone('Etc/GMT+5')) - checking.checking_start).total_seconds()
            minutes = float(difference_t) / 60
            if checking.confirmed == 1:
                if minutes > float(15):
                    checking.confirmed = 4
                    checking.save()
                    lat = checking.order.lat
                    long = checking.order.long
                    near_equipments = find_near_cron(float(lat), float(long))
                    order = checking.order
                    for i in near_equipments:
                        profile_renter = Profile.objects.get(id=i["renter_id"])
                        renter_chekings = OrderChecking.objects.filter(renter=profile_renter.user)
                        if checking not in renter_chekings:
                            start_new_checking = OrderChecking.objects.create(
                                renter=profile_renter.user,
                                equipment=RenterProduct.objects.get(id=i["product_id"]),
                                order=order,
                                confirmed=1,
                                checking_end=datetime.datetime.today()
                            )
                            start_new_checking.save()
    except:
        print("Something went wrong")
