import requests
import json


def send_sms(number, text, sms_id):
    """

    :param number: str; enter number without "+" sign, example: 998941234567
    :param text: str; enter text you want
    :param sms_id: int; sms id from backend
    :return:
    """
    username = "fastechnika"
    password = "M@4cVt$O3"

    url = "http://91.204.239.44/broker-api/send"
    data = {
        "messages": [
            {
                "recipient": f"{number}",
                "message-id": f"{sms_id}",
                "sms": {
                    "originator": "3700",
                    "content": {
                        "text": text
                    }
                }
            }]
    }
    r = requests.post(url, auth=(username, password), json=data)
    return r.text


# send_sms("998946128484", "function is running", 35)

def send_confirm_sms(renter, sms, start_time, end_time, price, address):
    renter_phone = renter.user.username
    sms_itself = sms.objects.create(
        phone_number=renter_phone,
        text=f"""You have new order, 
                                    price of order: UZS {price},
                                    start time: {start_time},
                                    end time: {end_time},
                                    """)
    send_sms(number=sms_itself.phone_number, text=sms_itself.text, sms_id=sms_itself.id)
    sms_itself.is_sent = 1
    sms_itself.save()


def send_accepted_sms(customer, sms, start_time, end_time, price, address):
    customer_phone = customer.username
    sms_itself = sms.objects.create(phone_number=customer_phone,
                                    text=f"""Your order is accepted, 
                                    price of order: UZS {price},
                                    start time: {start_time},
                                    end time: {end_time},
                                    """)
    print(
        "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
    send_sms(number=sms_itself.phone_number, text=sms_itself.text, sms_id=sms_itself.id)
    sms_itself.is_sent = 1
    sms_itself.save()
