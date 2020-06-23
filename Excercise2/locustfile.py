"""Скрипт нагрузочного тестирования."""

from locust import HttpUser, task, between
from random import choice
import json
import rstr


class UserBehavior(HttpUser):
    """Класс, описывающий поведение пользователя."""

    wait_time = between(1, 10)

    @task(1)
    def writing(self) -> None:
        """Отправка POST-запросов для записи данных в БД."""
        statuses = ["обрабатывается", "выполняется", "доставлено"]
        data = {"identifier": rstr.xeger(r'^[a-z0-9]{2,5}$'),
                "status": choice(statuses)}
        json_data = json.dumps(data, ensure_ascii=False)
        self.client.post("/write", json_data.encode('utf-8'))

    @task(5)
    def reading(self) -> None:
        """Отправка GET-запросов для чтения данных из БД."""
        self.client.get("/read")
