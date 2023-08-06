import json
import requests





def trigger(jenkins_config):

    jenkins_job_name = jenkins_config.jenkins_job_name        
    Jenkins_url = jenkins_config.Jenkins_url
    jenkins_user = jenkins_config.jenkins_user
    jenkins_pwd = jenkins_config.jenkins_pwd
    buildWithParameters = jenkins_config.buildWithParameters
    jenkins_params = jenkins_config.jenkins_params


    auth= (jenkins_user, jenkins_pwd)
    crumb_data= requests.get("{0}/crumbIssuer/api/json".format(Jenkins_url),auth = auth,headers={'content-type': 'application/json'})
    
    if str(crumb_data.status_code) == "200":

        if buildWithParameters:
            data = requests.get("{0}/job/{1}/buildWithParameters".format(Jenkins_url,jenkins_job_name),auth=auth,params=jenkins_params,headers={'content-type': 'application/json','Jenkins-Crumb':crumb_data.json()['crumb']})
        else:
            data = requests.get("{0}/job/{1}/build".format(Jenkins_url,jenkins_job_name),auth=auth,params=jenkins_params,headers={'content-type': 'application/json','Jenkins-Crumb':crumb_data.json()['crumb']})

        if str(data.status_code) == "201":
            jenkins_job_status = "Jenkins Deploy Jenkins job is triggered"

        else:
            jenkins_job_status = "Failed to trigger the Jenkins job"
    
    else:
        jenkins_job_status = "Couldn't fetch Jenkins-Crumb"
        
        raise 

                                   
    return {
        'statusCode': 200,
        'status': jenkins_job_status
    }
