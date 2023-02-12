import json
import random

from locust import task, between, SequentialTaskSet
from locust.contrib.fasthttp import FastHttpUser


def getRandomIndex():
    return random.randint(1000000, 9999999)


class ProductTasks(SequentialTaskSet):
    # @property
    # def vars(self):
    #     return self.vars

    wait_time = between(1, 3)

    @task
    def login(self):
        requestData = {"email": "cp@cp.cp", "password": "qwer1234"}
        url = '/v1/login'
        with self.client.post(url, requestData, catch_response=True) as resp:
            if resp.status_code == 200 and len(resp.json()) > 0:
                resp.success()
                ProductList.header["authorization"] = resp.json()["token"]
                print('当前token的值为', ProductList.header["authorization"])

            else:
                resp.failure('登录成功')

    @task
    def getSupplierList(self):
        url = '/v1/supplier/list'
        requestData = {"pagination": {"pageIndex": 1, "pageSize": 10}}
        json_str = json.dumps(requestData)
        with self.client.post(url, json_str, headers=ProductList.header, catch_response=True) as resp:
            if resp.status_code == 200 and len(resp.json()["supplier"]) > 0:
                resp.success()
                ProductList.first_supplier_id = resp.json()["supplier"][0]["sid"]
                print("first supplier id is :", resp.json()["supplier"][0]["sid"])
            else:
                print("get supplier failed")

    @task
    def getProductList(self):
        url = '/v1/product/list'
        requestData = {"pagination": {"pageIndex": 1, "pageSize": 10}}
        json_str = json.dumps(requestData)
        with self.client.post(url, json_str, headers=ProductList.header, catch_response=True) as resp:
            if resp.status_code == 200 and len(resp.json()["detail"]) > 0:
                resp.success()
            else:
                print("get product failed")

    @task
    def addNewProduct(self):
        url = '/v1/product/add'
        requestData = {
            "basic": {
                "stockStatus": bool(1),
                "imageList": [
                    "https://upcdn.io/FW25axR/raw/uploads/2022/11/13/OIP-C-3yUQ.jpeg"
                ],
                "sid": f"{ProductList.first_supplier_id}",
                "name": f"locust_add_product{getRandomIndex()}",
                "upc": "1234",
                "thumbnail": "https://upcdn.io/FW25axR/raw/uploads/2022/11/13/OIP-C-3yUQ.jpeg",
                "description": "locust api add product!"
            },
            "pricing": {
                "currency": "￥",
                "suggestedUnitPrice": 20,
                "minUnitPrice": 15,
                "maxUnitPrice": 25,
                "moq": 10000,
                "unit": "袋",
                "allowCustomerOffer": bool(1),
                "customerMinPrice": 18,
                "customerSuggestedPrice": 27
            },
            "attributes": {
                "type": "食品",
                "oem": "中国",
                "netContent": "300g",
                "originPlace": "中国大陆",
                "shelfLife": "12个月",
                "packaging": "袋装",
                "certification": "HACCP",
                "storage": "0-4°C冷藏",
                "category": "冷冻食品",
                "tags": [
                    "畅销",
                    "优惠",
                    "爆款"
                ],
                "buyMessage": "<p>api testing&nbsp;&nbsp;</p>"
            },
            "supplier": {}
        }
        json_str = json.dumps(requestData)
        with self.client.post(url, json_str, headers=ProductList.header, catch_response=True) as resp:
            if resp.status_code == 200 and len(resp.json()["detail"]) > 0:
                resp.success()
                ProductList.new_product_sku = resp.json()["detail"]["basic"]["sku"]
                print("新增产品为：", resp.json()["detail"])
            else:
                resp.failure('登录成功')

    @task
    def getProductDetail(self):
        url = f'/v1/product/detail/{ProductList.new_product_sku}'
        with self.client.get(url, headers=ProductList.header, catch_response=True) as resp:
            if resp.status_code == 200 and len(resp.json()["detail"]) > 0:
                resp.success()
                print("当前产品详情为：", resp.json()["detail"])
            else:
                print("get supplier failed")

    @task
    def updateProduct(self):
        url = f'/v1/product/update'
        requestData = {
            "basic": {
                "sid": f"{ProductList.first_supplier_id}",
                "sku": f"{ProductList.new_product_sku}",
                "name": f"locust_update_product{getRandomIndex()}",
                "thumbnail": "https://upcdn.io/FW25axR/raw/uploads/2022/11/13/OIP-C-3yUQ.jpeg",
                "description": "this data created by API",
                "upc": "1234",
                "imageList": [
                    "https://upcdn.io/FW25axR/raw/uploads/2022/11/13/OIP-C-3yUQ.jpeg"
                ],
                "pdf": None,
                "files": [],
                "stockStatus": bool(1),
                "state": 0,
                "createdAt": "1666893747",
                "updatedAt": "1667881493"
            },
            "pricing": {
                "minUnitPrice": 15,
                "maxUnitPrice": 25,
                "suggestedUnitPrice": 20,
                "allowCustomerOffer": bool(1),
                "customerMinPrice": 18,
                "customerSuggestedPrice": 27,
                "moq": 10000,
                "currency": "￥",
                "unit": "袋"
            },
            "attributes": {
                "type": "食品",
                "originPlace": "中国大陆",
                "shelfLife": "12个月",
                "packaging": "袋装",
                "certification": "HACCP",
                "storage": "0-4°C冷藏",
                "oem": "中国",
                "netContent": "300g",
                "buyMessage": "<p>api testing&nbsp;&nbsp;</p>",
                "category": "冷冻食品",
                "tags": [
                    "畅销",
                    "优惠",
                    "爆款"
                ]
            },
            "supplier": {
                "supplierId": "1",
                "supplierName": "CP Group",
                "supplierLogo": "/assets/cp-avatar.png",
                "supplierProductQuantity": 37,
                "supplierFollowerNumber": 684
            }
        }
        json_str = json.dumps(requestData)
        with self.client.post(url, json_str, headers=ProductList.header, catch_response=True) as resp:
            if resp.status_code == 200 and len(resp.json()["detail"]) > 0:
                resp.success()
            else:
                print("get supplier failed")

    @task
    def deleteProduct(self):
        url = '/v1/product/delete'
        requestData = {"sku": f"{ProductList.new_product_sku}"}
        json_str = json.dumps(requestData)
        with self.client.post(url, json_str, headers=ProductList.header, catch_response=True) as resp:
            if resp.status_code == 200 and resp.json()["ok"] == bool(1):
                resp.success()
            else:
                print("get supplier failed")


class ProductList(FastHttpUser):
    wait_time = between(1, 3)
    # vars = None
    tasks = [ProductTasks]
    host = 'https://dev.cpx.world'
    header = {
        "content-type": "application/json;text/plain; charset=utf-8",
        "authorization": "test"
    }
    first_supplier_id = None
    new_product_sku = None

    # def on_start(self):
    #     self.vars = {
    #         'email': 'cp@cp.cp',
    #         'password': 'qwer1234'
    #     }
    #     url = '/v1/login'
    #     requestData = {"email": self.vars['email'], "password": self.vars['password']}
    #     with self.client.post(url, requestData, catch_response=True) as resp:
    #         if resp.status_code == 200 and len(resp.json()) > 0:
    #             resp.success()
    #             ProductList.header["authorization"] = resp.json()["token"]
    #             print('当前token的值为', ProductList.header["authorization"])
    #
    #         else:
    #             resp.failure('登录成功')
