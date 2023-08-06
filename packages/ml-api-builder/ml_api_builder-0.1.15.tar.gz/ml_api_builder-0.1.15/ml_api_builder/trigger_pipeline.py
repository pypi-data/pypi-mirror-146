import json
import requests


jenkins_job_name = "dbx_daipe_demo_1"              
Jenkins_url = "http://18.185.104.16:8080"
jenkins_user = "m"
jenkins_pwd = "mlopsdbx1020"
buildWithParameters = False
jenkins_params = {'token': '-/9}u_N>O[^V7KTxWw%%;&Wz[n97^X'}


def trigger():
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
            print("Failed to trigger the Jenkins job")
            jenkins_job_status = "Failed to trigger the Jenkins job"
    
    else:
        print("Couldn't fetch Jenkins-Crumb")
        jenkins_job_status = "Couldn't fetch Jenkins-Crumb"
        
        raise 

    print(crumb_data)  
                                   
    return {
        'statusCode': 200,
        'status': jenkins_job_status
    }
