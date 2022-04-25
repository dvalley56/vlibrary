from trycourier import Courier

client = Courier(auth_token="YOUR AUTH TOKEN")

def send_email(email, template, data):
    resp = client.send_message(
        message={
            "to": {
                "email": email,
            },
            "template": template,
            "data": data,
        }
    )
    return resp
