from re import T
import requests
import pandas as pd
import time

from request_api import make_request
from status import JenkinsJob
from trigger_pipeline import trigger

class TestAPI():
    def __init__(self) -> None:
        pass

    def deploy_code(self):

        data = trigger()
        status = data.get('status')
        print(status)
        time.sleep(10)
        
        while 'job is triggered' in status  or 'job is building' in status:
            status = self.get_jenkins_job_status()
            time.sleep(5)
            
        return status
     
    def get_jenkins_job_status(self):

        jj = JenkinsJob()
        status = jj.jenkins_job_status()
        # print('status is ',status)

        return status
        
    def test_api(self, df: pd.DataFrame, api_url):

        dfj = df.to_json()
        r = requests.post(url = api_url, data = dfj)
        data = r.content

        return data


if __name__ == "__main__":
    ta = TestAPI()
    ta.deploy_code()