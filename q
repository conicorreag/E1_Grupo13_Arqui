[1mdiff --git a/app/api/routes.py b/app/api/routes.py[m
[1mindex bd6d777..c09cad3 100644[m
[1m--- a/app/api/routes.py[m
[1m+++ b/app/api/routes.py[m
[36m@@ -105,7 +105,7 @@[m [masync def purchase_request(request: Request, db: Session = Depends(database.get_[m
     print(response)[m
     if (transaction.status != "rejected"):[m
         send_request(data, transaction,response["token"])[m
[31m-    return {"url":response["url"],"request_id":transaction.request_id,"token":response["token"]}[m
[32m+[m[32m    return json.dumps({"url":response["url"],"request_id":transaction.request_id,"token":response["token"]})[m
 [m
 [m
 def send_request(data, transaction,token):[m
