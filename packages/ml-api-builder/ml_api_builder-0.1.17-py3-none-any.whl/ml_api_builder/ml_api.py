from re import T
import requests
import pandas as pd
import time

from .request_api import make_request
from .status import JenkinsJob
from .trigger_pipeline import trigger
from .api_config import ml_config, jenkins_config

# from request_api import make_request
# from status import JenkinsJob
# from trigger_pipeline import trigger

class TestAPI():
    def __init__(self, api_jenkins_config, api_ml_config) -> None:
        self.jenkins_config = api_jenkins_config
        self.ml_config = api_ml_config
        self.jenkins_job = JenkinsJob(self.jenkins_config)

        

    def deploy_code(self):

        data = trigger(self.jenkins_config)
        status = data.get('status')
        time.sleep(10)
        
        while 'job is triggered' in status  or 'job is building' in status:
            status = self.get_jenkins_job_status()
            time.sleep(5)

        output_log, url = self.get_jenkins_job_output_and_url()
        return status
        


    def get_jenkins_job_status(self):

        status = self.jenkins_job.jenkins_job_status()

        return status

    
    def get_jenkins_job_output_and_url(self):

        output = self.jenkins_job.job_output_log
        url = self.jenkins_job.api_url

        return output, url
        
    
    def test_api(self, df: pd.DataFrame, api_url):

        dfj = df.to_json()
        r = requests.post(url = api_url, data = dfj)
        data = r.content

        return data


if __name__ == "__main__":
    pass
