from locust import TaskSet, HttpUser, task
from core.environment.host import get_host_for_locust_testing


class ExploreUvlBehaviour(TaskSet):
    def on_start(self):
        self.load()

    @task
    def load(self):
        
        response = self.client.get("/exploreuvl")
        if response.status_code != 200:
            print(f"Request failed with status code: {response.status_code}")

class SearchBehaviour(TaskSet):
    def on_start(self):
        self.search()

    @task
    def search(self):
        
        response = self.client.get("/exploreuvl?query=author")
        if response.status_code != 200:
            print(f"Request failed with status code: {response.status_code}")
    

class ExploreUvlUser(HttpUser):
    tasks = [ExploreUvlBehaviour, SearchBehaviour]
    min_wait = 5000
    max_wait = 9000
    host = get_host_for_locust_testing()