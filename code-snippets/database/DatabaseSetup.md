# Steps to Setup Database

## Step 1
1. Install DBeaver Community
    - https://dbeaver.io/download/
## Step 2
1. Install mariaDB (I used Windows, I'm not sure if its a different set up for Mac and Lunix)
   - Windows: https://mariadb.org/download/?t=mariadb&p=mariadb&r=12.0.2&os=windows&cpu=x86_64&pkg=msi&mirror=acorn
   - Mac:
       - 'brew install mariadb'
       - 'brew services start mariadb'
         
   - Linux:
       - 'sudo apt update'
       - 'sudo apt install mariadb-server'
       - 'sudo systemctl start mariadb'
       - 'sudo systemctl enable mariadb'
 
2. When setting up the server keep the generic settings
    - For the password set it to "password"
## Step 3
1. Open DBeaver
2. Slightly left from the top middle click Database
3.  Click New Database Connection
4.  Choose MariaDB and hit next
5.  In the Database box write "Kama"
6.  In the password box write "password"
7.  Click Test Connection
8.  If connection goes through click Finish
9.  Run the databaseScript.sql in MariaDB

## Step 4
1. Run the connection.py script
2. Database should be connected!

