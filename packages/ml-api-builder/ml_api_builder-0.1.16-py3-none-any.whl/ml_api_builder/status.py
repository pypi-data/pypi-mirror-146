import json
import requests
import time


class JenkinsJob():
    def __init__(self, jenkins_config) -> None:
        self.jenkins_job_name = jenkins_config.jenkins_job_name        
        self.Jenkins_url = jenkins_config.Jenkins_url
        self.jenkins_user = jenkins_config.jenkins_user
        self.jenkins_pwd = jenkins_config.jenkins_pwd
        self.buildWithParameters = jenkins_config.buildWithParameters
        self.jenkins_params = jenkins_config.jenkins_params
                
        
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
                                        print ("Jenkins Deploy Job is success")
                                        return self.jenkins_console_output() # "Jenkins Deploy Job is success" # tr.send_request()
                                    else:
                                        print(self.jenkins_console_output())
                                        print( "Jenkins Deploy Job status failed")
                                        return self.jenkins_console_output() # "Jenkins Deploy Job status failed"

                    
            except Exception as e:
                    print (str(e))
                    return False


    def jenkins_console_output(self):
        auth= (self.jenkins_user, self.jenkins_pwd)
        r = requests.get(
                            "{0}/crumbIssuer/api/json".format(f"{self.Jenkins_url}/job/{self.jenkins_job_name}/lastBuild/consoleText"),
                            auth = auth,
                            headers={'content-type': 'application/json'})

        data = r.content.decode('utf-8','ignore')
        end_of_log = data[-1_500:]

        return end_of_log


if __name__ == "main":
    pass