import random
from transbank.error.transbank_error import TransbankError
from transbank.webpay.webpay_plus.transaction import Transaction


URL_COMPRA = "https://webhook.site/d6883dbb-d806-491e-b313-c6c622d3ee7b"
URL_2 ="localhost:3000/compraDetalle/"

async def webpay_plus_create(transaction_id,amount):
    print("Webpay Plus Transaction.create")

    session_id = str(random.randrange(1000000, 99999999))
    amount = random.randrange(10000, 1000000)
    response = (Transaction()).create(str(transaction_id), session_id, amount, URL_2)
    return {"token":response["token"],
           "url":response["url"]}

async def webpay_plus_commit(token):
    print("commit for token_ws: {}".format(token))
    response =  (Transaction()).commit(token=token)
    print("response: {}".format(response))
    print(f'response code : {response["response_code"]}')
    if response["response_code"] is not None:
        if response["response_code"] == 0:
            return "approved",token
        else:
            return "rejected",token
    else:
        return "user canceled",False
   



