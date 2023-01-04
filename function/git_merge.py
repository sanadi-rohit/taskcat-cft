import json
import logging
import requests
import boto3
import os

# set logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


# setup client
region = os.environ['AWS_REGION']
ssm = boto3.client('ssm', region_name=region)
code_pipeline = boto3.client('codepipeline', region_name=region)


def put_job_success(job, message):
    """Notify CodePipeline of a successful job
    Args:
        job: The CodePipeline job ID
        message: A message to be logged relating to the job status
        
    Raises:
        Exception: Any exception thrown by .put_job_success_result()
    
    """
    print('Putting job success')
    print(message)
    code_pipeline.put_job_success_result(jobId=job)
  
def put_job_failure(job, message):
    """Notify CodePipeline of a failed job
    Args:
        job: The CodePipeline job ID
        message: A message to be logged relating to the job status  
    Raises:
        Exception: Any exception thrown by .put_job_failure_result()  
    """
    print('Putting job failure')
    print(message)
    code_pipeline.put_job_failure_result(jobId=job, failureDetails={'message': message, 'type': 'JobFailed'})

def lambda_handler(event, context):
    """
    The Lambda function handler
    
    Merge the develop branch into master branch of the github repo.
    
    Args:
        event: The event passed by Lambda
        context: The context passed by Lambda
        
    """
    logger.debug("EVENT: " + str(event))
    try:
        # Extract the Job ID
        job_id = event['CodePipeline.job']['id']
        # Construct merge endpoint
        merge_endpoint = 'https://api.github.com/repos/{owner}/{repo}/merges'
        merge_endpoint = merge_endpoint.format(owner='NursultanBeken', repo='cfn_ci_cd')
        github_token = os.environ['GITHUBTOKEN']

        # Construct post data
        data = {
            'base': 'master',
            'head': 'dev',
            'commit_message': 'Shipped new feature from dev!'
            }
            
        # Construct header
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'token  ' + github_token
        }
            
        # Submit request
        result = requests.post(merge_endpoint, data=json.dumps(data), headers=headers)
        logger.debug(result) 
        if result.status_code == requests.codes['created']:
            # Merge completed successfully.
            logger.info('Merge completed successfully!')
            put_job_success(job_id, 'Merge complete!')
        elif result.status_code == requests.codes['no_content']:
            # Merge not needed. Base already contains the head, nothing to merge.
            logger.info('Nothing to merge!')
            put_job_success(job_id, 'Nothing to merge!')
        else:
            # Merge failed.
            logger.error(str(result.raise_for_status()))
            put_job_failure(job_id, 'Merge failed: ' + result.status_code)

    except Exception as e:
        # If any other exceptions which we didn't expect are raised
        # then fail the job and log the exception message.
        logger.info('Function failed due to exception.') 
        logger.error(e)
        put_job_failure(job_id, 'Function exception: ' + str(e))
    
    logger.info("Function execution complete")
    return True