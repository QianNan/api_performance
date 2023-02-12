import json
import random

from locust import task, between, SequentialTaskSet
from locust.contrib.fasthttp import FastHttpUser


def getRandomIndex():
    return random.randint(1000000, 9999999)


class SupplierTasks(SequentialTaskSet):
    wait_time = between(1, 3)

    @task
    def registerUser(self):
        emailName = f"apiLocustTest{getRandomIndex()}@cpx.com"
        requestData = {"user": {"name": emailName, "nickname": emailName, "type": 1,
                                "email": emailName, "password": "123Locust", "avatar": "", "gender": 0,
                                "introduce": ""}}

        url = '/v1/register'
        json_str = json.dumps(requestData)
        with self.client.post(url, json_str, headers=RegisterSupplier.header, catch_response=True) as resp:
            if resp.status_code == 200 and len(resp.json()["token"]) > 0:
                resp.success()
                RegisterSupplier.header["authorization"] = resp.json()["token"]
            else:
                print("register failed")

    @task
    def addNewSupplier(self):
        url = '/v1/supplier/add'
        requestData = {
            "name": f"api_vendor{getRandomIndex()}",
            "description": "locust api_created_vendor test",
            "owner": "1",
            "state": "1",
            "logo": "https://cpx.cpgroup.top/assets/avatar.png",
            "background": "https://cpx.cpgroup.top/assets/cover.png"
        }
        json_str = json.dumps(requestData)
        with self.client.post(url, json_str, headers=RegisterSupplier.header, catch_response=True) as resp:
            print("add New Supplier json is -------", resp.json())
            if resp.status_code == 200 and len(resp.json()["sid"]) > 0:
                resp.success()
            else:
                print("add New Supplier failed")

    @task
    def getAllSupplierList(self):
        url = '/v1/supplier/list'
        requestData = {"pagination": {"pageIndex": 1, "pageSize": 10}}
        json_str = json.dumps(requestData)
        with self.client.post(url, json_str, headers=RegisterSupplier.header, catch_response=True) as resp:
            if resp.status_code == 200 and len(resp.json()["supplier"]) > 0:
                resp.success()
                RegisterSupplier.first_supplier_id = resp.json()["supplier"][0]["sid"]
                print("first supplier id is :", resp.json()["supplier"][0]["sid"])
            else:
                print("get supplier failed")

    @task
    def getSupplierDetail(self):
        url = f'/v1/supplier/detail/{RegisterSupplier.first_supplier_id}'
        with self.client.get(url, headers=RegisterSupplier.header, catch_response=True) as resp:
            if resp.status_code == 200 and len(resp.json()["supplier"]) > 0:
                resp.success()
                print("first supplier id is :", resp.json()["supplier"]["sid"])
                print("first supplier name is :", resp.json()["supplier"]["name"])
            else:
                print("get supplier detail failed")

    @task
    def getMySupplierList(self):
        url = '/v1/user/belong/supplier/list'
        requestData = {"pagination": {"pageIndex": 1, "pageSize": 10}}
        json_str = json.dumps(requestData)
        with self.client.post(url, json_str, headers=RegisterSupplier.header, catch_response=True) as resp:
            if resp.status_code == 200 and len(resp.json()) > 0:
                resp.success()
                print("my supplier id is :", resp.json())
            else:
                print("get supplier failed")


class RegisterSupplier(FastHttpUser):
    header = {
        "content-type": "application/json;text/plain; charset=utf-8",
        "authorization": "test"
    }
    first_supplier_id = None
    wait_time = between(1, 3)
    tasks = [SupplierTasks]
    host = 'https://svcs-dev.cpx.world'
