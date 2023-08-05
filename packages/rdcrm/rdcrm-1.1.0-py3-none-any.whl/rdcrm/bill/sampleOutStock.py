from requests import  *

'''
* 样品出库回写
* http://58.211.213.34:88/test/crmapi-demo/otherStock.php
'''
url = "http://58.211.213.34:3000/crmapi/add"
data = {
  "module": "otherStock",
  "data": [
    {
      "mainFields": {
        "customform13_no": "other_1",
        "account_no": "CUST22033169",
        "approvestatus": "",
        "last_name": "",
        "createdtime": "",
        "modifiedtime": "",
        "outdate": "",
        "express_no": "",
        "cf_4757": "",
        "cf_4758": "",
        "cf_4759": "",
        "cf_4760": "",
        "cf_4761": "",
        "cf_4762": "",
        "cf_4763": "",
        "cf_4764": "",
        "cf_4765": "",
        "cf_4766": ""
      },
      "detailFields": [
        {
          "product_no": "300201-18",
          "customform11_no": "",
          "quantity": "",
          "comment": "",
          "sf3557": "",
          "sf3135": "",
          "sf3346": ""
        }
      ]
    }
  ]
}
r = post(url=url, json=data)
res = r.json()
print(res)
