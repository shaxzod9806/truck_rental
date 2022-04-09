import requests

header = {"Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjM1MjYwNjc5LCJpYXQiOjE2MzQ4Mjg2NzksImp0aSI6IjRmNDI3NjA2M2IyYzRlZTE5ZjNiNWQwMGIyOGM2NDYzIiwidXNlcl9pZCI6NX0.31UxRLlLuwzbLCJXJtFfSWoe0tdz-uC-eklQyAyq1Hg"}
r = requests.get("http://127.0.0.1:8000/api/renter/user_profile", headers=header)
result = r.json()
print(r.json())

print(result[0]["username"])