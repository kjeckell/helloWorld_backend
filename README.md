### Overall Notes: ###
* Responses to the Design Task questions are in A-DesignTask
* Responses to the Code Task are in the B-CodeTask folders
* Requirements elaborated in the prompt are captured in Requirements.md
* Implemented mocks of many of the functions that would handle actual customer verification, file upload and queueing, and metering of API usage.
* The green highlighted items in the arch diagram (A-DesignTask folder) are implemented in the sample provided.

### Executing the code ###
Assumptions: Python3 and pip are installed (virtualenv or otherwise), bash/ksh is the terminal

1. Install Requirements
    
    ``$ pwd`` - /../helloWorld_backend
    
    ``$ cd B-CodeTask/app``
    
    ``$ pip install -r requirements.txt``

2. Start uvicorn webserver
   
   ``$ uvicorn main:app --reload``

3. Test API via Swagger
   * Navigate to http://localhost:8000/docs
   * Expand the POST /ingestLogs/ API (click)
   * Click "Try it out"
   * Populate `clientID` with any string - not currently validated
   * Click 'Add string item' and then 'Choose File'
   * Navigate to the `Tests` folder and select the .json or .txt file
     * if you want you can test with other .json or .txt files as well, it IS limited to those extensions for now though.
   * If you would like to test with both/more at the same time click 'Add string item" again and select another file
   * Once you have all files selected for testing - click Execute