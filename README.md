# SOSO Server

This repository contains the code for the new SOSO server.

## Run Locally

Clone the project

```bash
   git clone https://github.com/ENG4000-SOSO/New-SOSO-Server.git
```

Go to the project directory

```bash
    cd New-SOSO-Server
```

Create and activate a virtual environment

```bash
    python3 -m venv venv
    source venv/bin/activate
```

Install all dependencies in the virutal environment

```bash
    pip install -r requirements.txt
```

Run the project using uvicorn

```bash
    uvicorn app.main:app --reload
```

Open the browser at the following localhost URL to see the project

```bash
    https://127.0.0.1:8000
```

To check the Swagger UI docs, visit the following URL

```bash
    https://127.0.0.1:8000/docs
```

## Setting up Database
