
### This Guideline Provides documentation of resolved issues related to running the Code:

<!-- Linux OS -->

<!-- The order should be maintained!!! -->


1. #### Install the Project's required dependencies:

    Be in the Project's root directory (.../Algosciences) and run the following command:

     **` pip install -r requirements.txt `**  

    The above command will install the dependencies needed for the project and this includes:
    ( matplotlib for visualization, setuptools for modularization of the project files, and pytest for testing)




2.  #### Fixed the Problem (ModuleNotFoundError no module named 'search_algorithms):
   This error was as a result of modules not being loaded globally within the project's root directory for usage.

   Be in the Project's root directory (.../Algosciences) and run the following command:

    **` pip install -e . `**  

   This command will make use of the setup tools (setuptools==70.0.0) present in the requirements.txt and package the 
   project files that are supposed to be installed as modules globally within the project's root directory (.../Algosciences).

   Once the above conditions are satisfied; the project will be executed without errors be it server.py or client.py
   or tests directory files or visulisation directory file; any will do work correctly and as expected.



3. #### Run the server script and to begin execution of any client requests:
  Be in the Project's root directory (.../Algosciences) and run the following command:
   **` python3 server/server.py  `**



4. #### Run the client script to send requests to the server on port 7777:
   Be in the Project's root directory (.../Algosciences) and run the following command:
  **` python3 client/client.py  `**




<!-- addittional  -->
1. ### Optional and not included file => virtual environment:
   suppose you don't want to conflict with existing dependencies present in your system globally then do make use of virtual environment so that this project's dependencies will ba contained only within the virtual environment.

  1. ### run the following command to create a new virtual environment:
   Be in the Project's root directory (.../Algosciences) and run the following command:


    ( python3 -m venv 'name for your virtual environment' ) i.e :
     -> **` python3 -m venv myvenv `**   
      or

    **` pip install virtualenv `**  then run

    ( virtualenv 'name for your virtual environment' ) i.e:
     -> **` virtualenv myvenv  `**


   2. ### run the following command to activate the virtual environment :
   Be in the Project's root directory (.../Algosciences) and run the following command:
     **` source myvenv/bin/activate  `**



   3. ### when the virtual environment is installed successfully repeat below commands in order:
   Be in the Project's root directory (.../Algosciences) and run the following command:

    1. **` pip install -r requirements.txt `**  

     2. **` pip install -e . `** 

      3. **` python3 server/server.py  `**

      4.  **` python3 client/client.py `**




<!-- Daemon installation is covered in the (Code_Installation.pdf) document which was sent via email -->
<!-- below is the same version summary -->


#### create a file with an extension of .service i.e (string_search_server.service)
The service file can be created in a folder of your choice, I prefer Desktop:

  .../Desktop/services/string_search_server.service
<!-- command creating folder and the service file inside desktop dir -->

**` mkdir myservice  `**

<!-- change into the myservice dir -->
**` cd myservice  `**

<!-- create service file -->
**` touch string_search_server.service  `**

<!-- open the service file to copy the service code there; here I'm using gedit you can use text editor of your choice -->
**` gedit string_search_server.service  `**


#### copy the code below into the created service file exactly as it is:
Only replace 'shimmian' in '/home/shimmian/Desktop/Algoscience/server/server.py'
with the username of your host machine. Then  save the changes.

<!-- code begin -->

[Unit]
Description=client_server search string
After=network.target

[Service]
ExecStart=/usr/bin/python3  /home/shimmian/Desktop/PythonWebsocket/server/server.py
Restart=always
User=nobody
Group=nogroup
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target

<!--code end  -->

#### execute the below commands to finish deployment of the server as a system daemon:

<!-- copies the service to the system daemon(s) directory -->
1. **` sudo cp string_search_server.service   /etc/systemd/system/ `**


<!--reloads all system daemons so that our newly created daemon will get recognized  -->
2.  **` sudo systemctl daemon-reload  `**


<!-- enable the service to start on boot -->
3. **` sudo systemctl enable string_search_server.service `**
   

   <!-- start the service-->
4.  **` sudo systemctl start string_search_server.service `**



