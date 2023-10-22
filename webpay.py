import random
from transbank.error.transbank_error import TransbankError
from transbank.webpay.webpay_plus.transaction import Transaction


URL_COMPRA = ""

def webpay_plus_create(transaction_id,amount):
    print("Webpay Plus Transaction.create")

    session_id = str(random.randrange(1000000, 99999999))
    amount = random.randrange(10000, 1000000)
    response = (Transaction()).create(transaction_id, session_id, amount, URL_COMPRA)
    return {"token":response["token"],
           "url":response["url"]}

def webpay_plus_commit(data):
    token = data("token_ws")
    print("commit for token_ws: {}".format(token))

    response = (Transaction()).commit(token=token)
    print("response: {}".format(response))
    if response.response_code:
        if response.response_code == 0:
            return "approved",token
        else:
            return "rejected",token
    else:
        return "user canceled",False
   



