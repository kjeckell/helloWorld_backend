from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from typing import List, Any
import json
import boto3 #not used as we have AWS comms commented out

app = FastAPI()

class AWSIngestError(Exception):
        def __init__(self, message):
            super().__init__(message)

@app.post("/ingestLogs/")
async def upload_files(files: List[UploadFile], clientID: str):
    """
    Upload and process files in JSON or TXT format.

    This endpoint accepts a list of uploaded files, processes them based on their
    file type (JSON or TXT), and returns the processed data.

    Args:
        files (List[UploadFile]): A list of uploaded files to process.
        clientID: would be passed later via the bearer token and we can resolve the client jwt.io

    Returns:
        Dict[str, Union[str, List[Dict[str, Union[str, Any]]]]]: A dictionary containing
        information about the processed files. The structure is as follows:
        {
            "files": [
                {
                    "file_name": str,
                    "file_type": str (either 'json' or 'txt')
                },
                ...
            ]
        }

    Raises:
        JSONResponse: If there is an error in the uploaded files, such as invalid
        JSON format or an unsupported file format, an appropriate error response is returned.
    """

    # VERIFY THE BEARER TOKEN
    # METER THE REQUEST FOR COST/USAGE TRACKING

    results = []
    clientConfig = getClientConfig(clientID)

    for file in files:
        if file.filename.endswith('.json'):
            # Handle JSON files
            try:
                content = await file.read()
                data = json.loads(content.decode('utf-8'))
                try:
                    stage_in_s3_and_queue(data, file.filename, clientConfig)
                    results.append({"file_name": file.filename, "file_type": "json"})
                except:
                    raise AWSIngestError("Ingestion Error")
            except json.JSONDecodeError as e:
                return JSONResponse(content={"error": "Invalid JSON format"}, status_code=400)
            except AWSIngestError as e:
                # Something went wrong writing to AWS - may want to keep going in the future and just provide a digest of failures
                print(f"An error occurred: {e}")
                return({
                    "status": "An Error Occured",
                    "clientConfig": clientConfig,
                    "failedFile": file.filename
                })

        elif file.filename.endswith('.txt'):
            # Handle TXT files
            try:
                content = await file.read()
                text_data = content.decode('utf-8')
                try:
                    stage_in_s3_and_queue(text_data, file.filename, clientConfig)
                    results.append({"file_name": file.filename, "file_type": "txt"})
                except:
                    raise AWSIngestError("Ingestion Error")
            except Exception as e:
                return JSONResponse(content={"error": "Error reading TXT file"}, status_code=400)

        else:
            return JSONResponse(content={"error": "Unsupported file format"}, status_code=400)
    
    #TODO: build out response in standard format
    return ({
        "status" : "success",
        "files": results
        }) 

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)

def stage_in_s3_and_queue(file_bytes, filename, clientConfig):
    '''
    Leaving commented out the actual interaction with AWS as we don't have any real infrastructure
    and mocking this to allow the API for ingestion to function.

    This can be purposely failed by sending empty input values so you can raise the custom error
    '''
    # Initialize AWS S3 and SQS clients
    #s3_client = boto3.client('s3')
    #sqs_client = boto3.client('sqs')

    try:
        # Verify input params
        if any(arg is None for arg in (file_bytes, filename, clientConfig)):
            raise TypeError
        
        # Upload the bytes to S3
        #s3_client.put_object(Bucket=bucket_name, Key=object_key, Body=file_bytes)


        # Construct the S3 URL of the uploaded file
        s3_url = f"https://{clientConfig['clientS3Bucket']}.s3.amazonaws.com/stage/{filename}"
        
        # Place the S3 URL in SQS
        #response = sqs_client.send_message(
        #    QueueUrl=clientConfig["clientSQSQueue"],
        #    MessageBody={
        #        "s3Url": s3_url,
        #        "clientConfig": clientConfig
        #    }
        #)

        # Print a success message
        print(f"File uploaded to S3: {s3_url}")
        #print(f"Message sent to SQS with MessageId: {response['MessageId']}")
        print(f"Message sent to SQS with MessageId: ak3ka0402k214s")

    except Exception as e:
        print(f"Error uploading file to S3 or sending SQS message: {str(e)}")
    except TypeError as e:
        print(f"Mising Input Variables")

def getClientConfig(clientID: str):
    '''
    Fully mocked - allows us to raise the complexity of how/where we store data and name things
    without needing to really tinker with how this all works.

    Plan: Move this data to DynamoDB and make this function a query to that datatable
    '''
    return({
        "clientID" : clientID,
        "clientIndexPattern": clientID + '_09192023', #date based index, likely want to encode even the clientid for more security
        "clientRSTable": clientID + '_table', #assumes single cluster many tables
        "clientS3Bucket": clientID + '_3k30ak3K3k60', #random guid would be added for global names - each environment would be distinct
        "clientSQSQueue": clientID + "_sqs"
    })
