from requests import  *
url = "http://58.211.213.34:3000/crmapi/add"
data = {
  "module": "salesback",
  "data": [
      {
          "mainFields": {
              "salesback_no": "sales_back_01",
              "account_no": "CUST22033169",
              "approvestatus": "未提交",
              "salesorder_no": "XSDD3",
              "customform03_no": "",
              "currency_code": "CNY",
              "last_name": "系统管理员",
              "createdtime": "2022-03-13 16:53:19",
              "modifiedtime": "2022-03-13 16:53:19",
              "salesbackdate": "2022-03-13",
              "description": "",
              "cf_4767": "",
              "cf_4768": "",
              "cf_4769": "",
              "cf_4772": "",
              "cf_4770": "",
              "cf_4771": ""
          },
          "detailFields": [
              {
                  "product_no": "300201-18",
                  "quantity": "2",
                  "name": "总仓",
                  "comment": "",
                  "sf2080": "",
                  "sf2291": "",
                  "sf2713": "",
                  "sf2924": "",
                  "sf3768": "",
                  "sf3979": ""
              }
          ]
      },
{
          "mainFields": {
              "salesback_no": "sales_back_02",
              "account_no": "CUST22033169",
              "approvestatus": "未提交",
              "salesorder_no": "XSDD3",
              "customform03_no": "",
              "currency_code": "CNY",
              "last_name": "系统管理员",
              "createdtime": "2022-03-13 16:53:19",
              "modifiedtime": "2022-03-13 16:53:19",
              "salesbackdate": "2022-03-13",
              "description": "",
              "cf_4767": "",
              "cf_4768": "",
              "cf_4769": "",
              "cf_4772": "",
              "cf_4770": "",
              "cf_4771": ""
          },
          "detailFields": [
              {
                  "product_no": "300201-18",
                  "quantity": "2",
                  "name": "总仓",
                  "comment": "",
                  "sf2080": "",
                  "sf2291": "",
                  "sf2713": "",
                  "sf2924": "",
                  "sf3768": "",
                  "sf3979": ""
              }
          ]
      }
  ]
}
r = post(url=url, json=data)
res = r.json()
print(res)
