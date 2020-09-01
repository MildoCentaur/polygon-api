# polygon-api
polygon provider api with flask, docker, postgres, postgis 

#How to run the app

1) Download the the repository.  
2) Open a shell terminal and execute.
    
    ``docker-compose build && docker-compose up ``
    
3) The database will be initialized with some testing data.
 
4) In the postman folder you will find the collection if requests samples.

#How to run the tests
1)  Open a terminal or bash

2) Run the following commands to creatre the virtual environment
 
    `` pip3 install virtualenv``
    
    `` virtualenv venv --python=python3.7 ``
 
    `` source venv/bin/activate``
     
3) Install dependencies
 
    `` pip3 install --no-cache-dir -r requirements.txt``
    
4) Run the tests

    `` pytest tests``