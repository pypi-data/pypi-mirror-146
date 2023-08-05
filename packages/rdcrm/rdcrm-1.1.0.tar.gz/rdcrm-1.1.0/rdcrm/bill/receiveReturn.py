from requests import  *

'''
* 销售退款
* http://58.211.213.34:88/test/crmapi-demo/cashback.php
'''
url = "http://58.211.213.34:3000/crmapi/add"
data = {
  "module": "cashback",
  "data": [
    {
      "mainFields": {
        "cashback_no": "cashback_1",
        "account_no": "CUST22033169",
        "approvestatus": "",
        "last_name": "",
        "createdtime": "",
        "modifiedtime": "",
        "description": "",
        "cashbackdate": "",
        "cf_4778": "",
        "cf_4779": "",
        "cf_4780": "",
        "cf_4781": "",
        "cf_4782": "",
        "cf_4783": "",
        "cf_4784": "",
        "cf_4785": "",
        "cf_4786": "",
        "cf_4787": ""
      },
      "detailFields": [
        {
          "product_no": "300201-18",
          "salesorder_no": "",
          "quantity": "",
          "taxprice": "",
          "comment": "",
          "sf4401": "",
          "sf4612": "",
          "sf4823": "",
          "sf5034": "",
          "sf5245": "",
          "sf5456": "",
          "sf5667": "",
          "sf5878": "",
          "sf6089": "",
          "sf6300": "",
          "sf6511": "",
          "sf6722": "",
          "sf6933": ""
        }
      ]
    }
  ]
}
r = post(url=url, json=data)
res = r.json()
print(res)
