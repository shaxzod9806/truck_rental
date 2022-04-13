# import firebase_admin
# from firebase_admin import credentials, messaging
# from motochas import settings
import requests
import json


# cred = credentials.Certificate(settings.firebase_cred)
# firebase_admin.initialize_app(cred)


# def sendPush(title, msg, registration_token, dataObject=None):
#     message = messaging.MulticastMessage(
#         notification=messaging.Notification(title=title,
#                                             body=msg,
#                                             ),
#         data=dataObject,
#         tokens=registration_token
#     )
#
#     response = messaging.send_multicast(message)
#     print('successfully sent message', response)


def send_notification(title, body, fcm_token, image_url):
    request_body = {"to": fcm_token,

                    "notification": {
                        "title": title,
                        "body": body,
                        # "image": image_url
                    },
                    "data": {
                        # "url": image_url
                    }
                    }
    data = json.dumps(request_body)
    token = "key=AAAAeoexyh0:APA91bEmJYowPKaEsPzZ2xwmKkIcZcmVMJekvsTc3W-qwlA14MYF_kXKC4i04_bsZSWjcsTPze40L_9vvfxgfOdzRkJRROcxWFMEEDFBeTIlPBptFiIdLQDHC6S-bHp9WK7sLMNm6Inr"
    headers = {"Content-Type": "application/json", "Authorization": token}
    r = requests.post("https://fcm.googleapis.com/fcm/send", data=data, headers=headers)
    return r.json()


# print(send_notification("SIno uchun", "motochas v2 chiqdi",
#                         "e9_-MzJ3Se2VUhVnCFoLo3:APA91bHFIjL0zw0qqHvbmeFaYpfJMFXMnjpQBErPGSIlPIN8_pNpn4siVbP3fyA_lJYo_ohU1XtKiD8aBethRh_sqWkwTadzFWHQnKMaRk0wUq3iztyCfwyLM_RaZeW2q5qFnTdlKblK",
#                         "image_url"))
