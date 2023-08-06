import json
import requests
import time
import re

class JenkinsJob():
    def __init__(self, jenkins_config) -> None:
        self.jenkins_job_name = jenkins_config.jenkins_job_name        
        self.Jenkins_url = jenkins_config.Jenkins_url
        self.jenkins_user = jenkins_config.jenkins_user
        self.jenkins_pwd = jenkins_config.jenkins_pwd
        self.buildWithParameters = jenkins_config.buildWithParameters
        self.jenkins_params = jenkins_config.jenkins_params

        self.job_output_log = ''
        self.api_url = ''
                
        
    def jenkins_job_status(self):
            
            try:
                    auth= (self.jenkins_user, self.jenkins_pwd)
                    while True:
                            data = requests.get(
                                "{0}/crumbIssuer/api/json".format(f"{self.Jenkins_url}/job/{self.jenkins_job_name}/lastBuild/api/json"),
                                auth = auth,
                                headers={'content-type': 'application/json'}).json()

                            if data['building']:
                                    print('job is building')
                                    return 'job is building'
                            else:
                                    if data['result'] == "SUCCESS":
                                        self.job_output_log, self.api_url = self.jenkins_console_output_succed_job()
                                        return 'success'
                                    else:
                                        self.job_output_log, self.api_url = self.jenkins_console_output_fail_job()
                                        return  'fail'

                    
            except Exception as e:
                    print (str(e))
                    return False

    def jenkins_console_output_succed_job(self):
        auth= (self.jenkins_user, self.jenkins_pwd)
        r = requests.get(
                            "{0}/crumbIssuer/api/json".format(f"{self.Jenkins_url}/job/{self.jenkins_job_name}/lastBuild/consoleText"),
                            auth = auth,
                            headers={'content-type': 'application/json'})

        data = r.content.decode('utf-8','ignore')
        end_of_log = data[-1_500:]
        url = self.get_url(data)

        return end_of_log, url


    def jenkins_console_output_fail_job(self):
        auth= (self.jenkins_user, self.jenkins_pwd)
        r = requests.get(
                            "{0}/crumbIssuer/api/json".format(f"{self.Jenkins_url}/job/{self.jenkins_job_name}/lastBuild/consoleText"),
                            auth = auth,
                            headers={'content-type': 'application/json'})

        data = r.content.decode('utf-8','ignore')
        end_of_log = data[-1_500:]
        url = 'Job deploy failed, API was not deployed'

        return end_of_log, url

    def get_url(self, output):
        complete_url = ''

        try:
            found_url = re.search("YOU CAN CALL YOUR API IN THIS URL:\'(.+?)\' RUNNING ON AWS LAMBDA", output).group(1)
            complete_url = str(found_url+'/predict')
            return complete_url
        except AttributeError:
            not_found = 'Not able to find API url inside Jenkins job output log file' 
            return not_found



if __name__ == "main":
    pass