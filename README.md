# bale bot request manager 
Bale Bot Request Manager is a project that uses the APIs of the request manager project.
This is version 0.2.0


## The problems of this project that must be solved:
1-Fixing the user location problem in the admin panel
2- When the user sends a request, if the request was not completed yet and he only gave us the request ID and the request result button, click on the request result to show us the result (no need to enter the request ID).
3 - Returns the result of the requests that have not been returned to the user
4- Return the request ID to the user in a copyable form that can be easily copied in the mobile version
5- Request username and password to request the addition of two numbers

## Configuration
Before you start using this application, make sure to update the configurations in the `.env` file. Below are some important settings you need to modify:

First, you need to register in the request management application, Then put the username and password entered in the .env file in API_USERNAME and API_PASSWORD

Open the ".env" file and find the variables and change its values to the desire value.

1. **SYSTEM_NAME**

2. **DOMAIN_ADDRESS**

3. **TARGET_API_URL**

4. **API_USERNAME**

5. **API_PASSWORD**

6. **BOT_TOKEN**

7. **BASE_URL**

8. **BASE_FILE_URL**