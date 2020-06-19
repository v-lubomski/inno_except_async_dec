from locust import HttpUser, task, between
from random import randint, choice
import json


class UserBehavior(HttpUser):
    wait_time = between(2, 5)

    @task(1)
    def writing(self):
        statuses = ["Processing", "Executing", "Delivered"]
        # data = {randint(0, 10000): choice(statuses)}
        data = json.dumps({str(randint(0, 10000)): choice(statuses)})
        self.client.post("/write", data=data)

    @task(1)
    def reading(self):
        self.client.get("/read")


