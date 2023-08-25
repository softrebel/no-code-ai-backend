# No Code AI
Automation for machine learning model generation




## Requirements:
- python 3.11
- install dependencies using

```sh
[linux]   pip3 install -r requirements.txt
[windows]  pip install -r requirements.txt
```

- Copy `.env.sample` and rename it to `.env`. Then fill the variables
- Create MongoDb database with name `NoCodeAI`
- run command `python -m main` in the root folder.
- redis server. for development you can run docker command:
    `docker run -p 6379:6379 --name redis_service -d redis`


## Run
You can run this project in two ways:

1. Run in development:
    Just run file `main_dev.py` in your IDE to have debugging options.

2. Run in production:
    Execute this command in this directory:
    ```python
    python uvicorn main:app
    ```

Default Swagger Url:
http://127.0.0.1:8000/docs


## Endpoints
there 3 main endpoints:




## Seeds
there is on seed file in the `seeds` directory. You can edit this file to insert user in `user` collection if not exists.

Default user:

```
    username: admin
    password: admin
```

## Authentication
Use 'v1/auth' and pass username and password to issue token. after the token issued, use that in header key Authorization with prefix `Bearer ` for example:
`Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTY4NDI0NzM5Nn0.13ClZz0-KiwylTMQdGkRuF1mm5vFQsdfyVn_7kGPic0`





