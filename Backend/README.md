# GetFitGo

## Overview

GetFitGo is a fitness application with a backend implemented in Python using Flask. This README provides instructions on how to set up and run the backend server.

## How to Run Backend

### Prerequisites

Make sure you have the following installed on your machine:

- Python 3
- pip3

### Installation

Install the required Python packages using pip3. Open a terminal and run the following command:

```bash
pip3 install pymysql Flask flask_restful flask_swagger_ui flask_cors cryptography
```

### Database Configuration

In the `db.py` file, update the database credentials on lines 7-9 with your own information:

```python
# db.py
host = "your_host"
user = "your_username"
password = "your_password"
```

Make sure to set the correct values for `host`, `user`, and `password` based on your database configuration.

The database name for this project is "GetFitGo."

### Run the Backend

Navigate to the folder where the Python program is located and run the following command:

```bash
python3 main.py
```

This will start the backend server.

### Swagger API Documentation

Once the server is running, open your web browser and go to the following URL to view the Swagger API documentation:

```
http://127.0.0.1:5000/swagger/
```

Replace `5000` with the port on which your Python program is running. The Swagger file contains detailed information about all API responses and data types. Use the Swagger documentation to explore and understand the available endpoints and their functionalities.

That's it! You have successfully set up and run the GetFitGo backend.