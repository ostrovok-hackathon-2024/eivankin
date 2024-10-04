import random

import pandas as pd
from locust import HttpUser, TaskSet, between, task

data = pd.read_csv("./raw_data/rates_dirty.csv").fillna("undefined")
texts = data["rate_name"].tolist()


class UserBehavior(TaskSet):
    @task
    def infer_single(self):
        text = random.choice(texts)
        self.client.post("/infer/single", json={"text": text})

    @task
    def infer_batch(self):
        batch_size = random.randint(2, 5)
        random_texts = random.sample(texts, min(batch_size, len(texts)))
        self.client.post("/infer/batch", json={"texts": random_texts})


class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(0.1, 0.5)
