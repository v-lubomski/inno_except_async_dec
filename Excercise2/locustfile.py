from locust import HttpUser, task, between
from random import randint, choice
import json
import rstr


class UserBehavior(HttpUser):
    wait_time = between(1, 10)

    @task(1)
    def writing(self):
        statuses = ["обрабатывается", "выполняется", "доставлено"]
        data = {"identifier": rstr.xeger(r'^[a-z0-9]{2,5}$'), "status": choice(statuses)}
        json_data = json.dumps(data, ensure_ascii=False)
        self.client.post("/write", json_data.encode('utf-8'))

    @task(5)
    def reading(self):
        self.client.get("/read")

