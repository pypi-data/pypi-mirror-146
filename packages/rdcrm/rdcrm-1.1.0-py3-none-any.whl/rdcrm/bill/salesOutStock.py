from requests import  *
'''
* http://58.211.213.34:88/test/crmapi-demo/outboundorder.php
'''
url = "http://58.211.213.34:3000/crmapi/add"
data = {
  "module": "outboundorder",
  "data": [
    {
      "mainFields": {
        "out_no": "out_2",
        "account_no": "CUST22033169",
        "approvestatus": "未提交",
        "last_name": "系統管理員",
        "createdtime": "2022-03-13 16:53:19",
        "modifiedtime": "2022-03-13 16:53:19",
        "outdate": "2022-03-13",
        "express_no": "",
        "cf_4755": "",
        "cf_4749": "",
        "cf_4750": "",
        "cf_4751": "",
        "cf_4752": "",
        "cf_4756": "",
        "cf_4753": ""
      },
      "detailFields": [
        {
          "product_no": "300201-18",
          "salesorder_no": "XSDD3",
          "quantity": "2",
          "name": "总仓",
          "sf2080": "",
          "sf2291": "",
          "sf2713": "",
          "sf2924": ""
        }
      ]
    }
  ]
}
r = post(url=url, json=data)
res = r.json()
print(res)
