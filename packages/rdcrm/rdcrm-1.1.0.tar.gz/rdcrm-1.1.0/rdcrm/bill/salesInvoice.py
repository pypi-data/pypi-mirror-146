from requests import  *

'''
* 销售发票申请
* http://58.211.213.34:88/test/crmapi-demo/invoice.php
'''
url = "http://58.211.213.34:3000/crmapi/add"
data = {
  "module": "invoice",
  "data": [
      {
          "mainFields": {
              "invoice_no": "in_1",
              "account_no": "CUST22033169",
              "approvestatus": "",
              "last_name": "",
              "createdtime": "",
              "modifiedtime": "",
              "invoicedate": "",
              "invoicetype": "",
              "invoice_num": "",
              "express_company": "",
              "express_no": "",
              "invoicestatus": "",
              "description": ""
          },
          "detailFields": [
              {
                  "product_no": "300201-18",
                  "salesorder_no": "",
                  "quantity": "",
                  "taxprice": "",
                  "tax_amount": "",
                  "discount_percent": "",
                  "discount_amount": "",
                  "actualtaxprice": "",
                  "comment": ""
              }
          ]
      }
  ]
}
r = post(url=url, json=data)
res = r.json()
print(res)
