from locust import TaskSet, HttpUser, task
from core.environment.host import get_host_for_locust_testing


class ExploreUvlUser(TaskSet):
    def on_start(self):
        self.index()

    @task
    def submit_search_form(self):
        
        response = self.client.get("/polls/2/vote")
        csrftoken = response.cookies['csrftoken']

        json_data = {
            'csrf_token': csrftoken,
            'query': '',
            'title': '',
            'description': '',
            'authors': '',
            'q_tags': '',
            'bytes': '',
            'publication_type': 'any'
        }

        response = self.client.post('/exploreuvl', json=json_data)

        if response.status_code != 200:
            print(f"Request failed with status code: {response.status_code}")


class ExploreUvlUser(HttpUser):
    tasks = [ExploreUvlUser]
    min_wait = 5000
    max_wait = 9000
    host = get_host_for_locust_testing()