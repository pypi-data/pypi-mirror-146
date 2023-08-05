from requests import  *
url = "http://58.211.213.34:3000/crmapi/add"
data = {
  "module": "salesStatement",
  "data": [
      {
          "mainFields": {
              "customform05_no": "cus-05-01",
              "account_no": "CUST22033169",
              "approvestatus": "未提交",
              "last_name": "",
              "createdtime": "",
              "modifiedtime": "",
              "cf_4740": "",
              "cf_4741": "",
              "cf_4742": "",
              "cf_4743": "",
              "cf_4744": "",
              "cf_4745": "",
              "cf_4746": "",
              "cf_4747": "",
              "cf_4748": ""
          }
      }
  ]
}
r = post(url=url, json=data)
res = r.json()
print(res)
