from trycourier import Courier

client = Courier(auth_token="pk_prod_QAJ2SS4BY54HSPHVFJHX5W3EJ131")

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
