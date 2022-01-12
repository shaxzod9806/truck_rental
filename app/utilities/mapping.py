from math import radians, cos, sin, asin, sqrt
from renter.models import RenterProduct
from utilities.models import SMS
from utilities.sms import send_sms


def dist(lat1, long1, lat2, long2):
    lat1, long1, lat2, long2 = map(radians, [lat1, long1, lat2, long2])
    dlon = long2 - long1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    km = 6371 * c
    return km


def find_min(kilometers):
    min_km = kilometers[0]["km"]
    renter_id = 0
    product_id = 0
    for i in kilometers:
        km_itself = i["km"]
        if min_km > km_itself:
            min_km = km_itself
            renter_id = i["renter_id"]
            product_id = i["product_id"]
        else:
            pass
    return {"km": min_km, "renter_id": renter_id, "product_id": product_id}


def find_near_equipment(user_lat, user_long):
    renter_products = RenterProduct.objects.all().values()
    kms = []
    for equipment in renter_products:
        lat = equipment["latitude"]
        long = equipment["longitude"]
        km = dist(lat, long, user_lat, user_long)
        renter_id = equipment["renter_id"]
        product_id = equipment["id"]
        mini_dict = {"product_id": product_id, "renter_id": renter_id, "km": km}
        kms.append(mini_dict)
    minimum = find_min(kms)
    return minimum

# user_lat = 41.31090537318465
# user_long = 69.28148097265912
# kms = [{'product_id': 1, 'renter_id': 1, 'km': 7.437136503158664},
#        {'product_id': 2, 'renter_id': 2, 'km': 9.698823436980804},
#        {'product_id': 3, 'renter_id': 6, 'km': 6.035135925644598},
#        {'product_id': 4, 'renter_id': 7, 'km': 6.237550424552983}]




