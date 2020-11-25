# Favorites API

Favorites-API is the back-end responsible for storing the favorite products of the Magalu customers.

## Description

This API store customers and its favorite products from Luizalabs products API, so this API works communicating with an external API.

To avoid high use of external resources and improve performance, the results of Luizalabs products API are stored in cache for a configurable amount of time.

## Requirements:

- Python (Tested and developed on 3.9)
- [Poetry](https://python-poetry.org/docs/#installation)
- [Redis](https://redis.io/topics/quickstart)
- [PostgreSQL](https://www.postgresql.org/download/)

## Setup project

To setup the project just follow these steps.

1. Start environment variable files.

    This project uses environment variables to load its settings, the template for this file is the `local.env` file. Favorites API will always search for the `.env` file so just run the following command

    ```sh
    cp local.env .env
    ```

2. Edit the environment variables on `.env`.

    - DEBUG: Defines if the API will run in Debug mode or not (Set False in production)
    - SECRET_KEY: Django secret key
    - DATABASE_URL: Database URL, configure with local production postgreSQL URL.
    - REDIS_URL: The URL to connect at redis.
    - FAVORITES_EXPIRE_TIMEOUT: Timeout in seconds that API will use to store external API response on cache
    - LUIZALABS_API_URL: The URL of external Luizalabs API

3. Install project virtual environment.

    To install the virtual environment, use Poetry with the following command
    ```sh
    Poetry install
    ```

    To activate the virtual environment use:
    ```sh
    Poetry shell
    ```

4. Run Migrations

    If this is the first time you are running Favorites API, you must run the migrations command
    ```sh
    python favorites-api/manage.py migrate
    ```
    This command will start the project structure in the database.

5. Create new user

    Every service that will consume Favorites API must have its user created using manage commands. To create a new user, run the following command:

    ```sh
    python favorites-api/manage.py create_user <Username> <Password>
    ```

    For security its recommended to use a big password, you can access this site: https://passwordsgenerator.net/ to generate a 32 or 64 characters password.

    To update the password you can use the `update_password` command


6. Run the project

    To run the project locally use the command
    ```sh
    python favorites-api/manage.py runserver 0:8000
    ```
    This command is using the port 8000 for example, but you can use other ports.

## Running tests

To run unit tests for the project there is a shortcut command on Makefile, run this command:
```sh
make test
```

## Rest API

The Favorites API is described below

### Authenticate

#### Request
`POST v1/auth/`
```sh
curl --request POST \
  --url http://localhost:8000/v1/auth/ \
  --header 'Content-Type: application/json' \
  --data '{
        "username":  "admin",
        "password": "admin"
    }'
```

#### Response

```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYwNjQxMDc4OSwianRpIjoiNzZkYjYwMDY5YmRmNDRmM2JmY2EzY2U4OTk5NjExMGUiLCJ1c2VyX2lkIjoyfQ.U8eQBrp2mX-UNcR7w0m_unJzexkNBPQX1WOjmqWCR5g",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjA2MzI0Njg5LCJqdGkiOiI4MjY1MmQyYmY4ZWY0NDAyOTViYmQ3N2I0N2RkMTY5MSIsInVzZXJfaWQiOjJ9.PaxjdZf4ywTGO9t9Mgci69J1CmFsGknwkoSPtHUX1JY"
}
```

### Refresh auth token

#### Request

`POST v1/auth/refresh/`
```sh
curl --request POST \
  --url http://localhost:8000/v1/auth/verify/refresh \
  --header 'Content-Type: application/json' \
  --data '{
	"username": "admin",
	"password": "admin",
	"token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYwNjQxMDc4OSwianRpIjoiNzZkYjYwMDY5YmRmNDRmM2JmY2EzY2U4OTk5NjExMGUiLCJ1c2VyX2lkIjoyfQ.U8eQBrp2mX-UNcR7w0m_unJzexkNBPQX1WOjmqWCR5g"
}'
```

#### Response

```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYwNjQxMzU1NywianRpIjoiNDJiMzNhODZlMDEwNGEyYWE5NGE2NGQyYTA5YzdmZDgiLCJ1c2VyX2lkIjoxfQ.5-Yc8ZV6bUXyljJpAfgmD3PtaXfaRQ9E1nOay8aqrIY",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjA2MzI3NDU3LCJqdGkiOiI0ODNiMGNiZDlhMjY0MjRkODM2YjhjMDQxZjIwNDc4OSIsInVzZXJfaWQiOjF9.xUo4GZChKCmStWWZxe1P27Q0mdcUwFZgviQ8A8Ms3is"
}
```

 ### Create Customer

 #### Request

 `POST v1/customers/`
 ```sh
curl --request POST \
  --url http://localhost:8000/v1/customers/ \
  --header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjA2MzI3NjEwLCJqdGkiOiI1MWMzNmYwZjc4Y2E0NWQxYmRiY2IyYzEyNDdmYzU0ZCIsInVzZXJfaWQiOjF9.HQw5tT8D6Q8RDXsGw3K-BufMLxz5kQKJCpdKi0vcAFI' \
  --header 'Content-Type: application/json' \
  --data '{
	"email":  "lucas.de.oliveira@outlook.com",
	"name": "Lucas de Oliveira"
}'
 ```

 #### Response

 ```json
{
  "id": "2022413e-b96f-4326-82d4-51377110c0f0",
  "name": "Lucas de Oliveira",
  "email": "lucas.de.oliveira@outlook.com",
  "created_at": "2020-11-25T18:02:00.572122Z",
  "updated_at": "2020-11-25T18:02:00.572153Z"
}
 ```

 ### Retrieve customer

 #### Request

`GET v1/customers/<id>`
```sh
curl --request GET \
  --url http://localhost:8000/v1/customers/2022413e-b96f-4326-82d4-51377110c0f0/ \
  --header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjA2MzMxNjEwLCJqdGkiOiJiYmNiMWI2NGJiMmE0OGRjODkwMmYxZTVmNTc3NDAwNSIsInVzZXJfaWQiOjF9.FwMS-r5GZUwXqozZjo9LcXLg5kkZmmefSjGQonvEaCY'
```

#### Response

```json
{
  "id": "2022413e-b96f-4326-82d4-51377110c0f0",
  "name": "Lucas de Oliveira",
  "email": "lucas.de.oliveira@outlook.com",
  "created_at": "2020-11-25T18:02:00.572122Z",
  "updated_at": "2020-11-25T18:02:00.572153Z"
}
```

### List Customers

#### Request

```sh
curl --request GET \
  --url http://localhost:8000/v1/customers/2022413e-b96f-4326-82d4-51377110c0f0/ \
  --header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjA2MzMxNjEwLCJqdGkiOiJiYmNiMWI2NGJiMmE0OGRjODkwMmYxZTVmNTc3NDAwNSIsInVzZXJfaWQiOjF9.FwMS-r5GZUwXqozZjo9LcXLg5kkZmmefSjGQonvEaCY'
```

#### Response

```json
[
  {
    "id": "2022413e-b96f-4326-82d4-51377110c0f0",
    "name": "Lucas de Oliveira",
    "email": "lucas.de.oliveira@outlook.com",
    "created_at": "2020-11-25T18:02:00.572122Z",
    "updated_at": "2020-11-25T18:02:00.572153Z"
  }
]
```

### Update Customer

#### Request

`PATCH v1/customers/<id>/`
```sh
curl --request PATCH \
  --url http://localhost:8000/v1/customers/2022413e-b96f-4326-82d4-51377110c0f0/ \
  --header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjA2MzMxNjEwLCJqdGkiOiJiYmNiMWI2NGJiMmE0OGRjODkwMmYxZTVmNTc3NDAwNSIsInVzZXJfaWQiOjF9.FwMS-r5GZUwXqozZjo9LcXLg5kkZmmefSjGQonvEaCY' \
  --header 'Content-Type: application/json' \
  --data '{
	"name": "Lucas Oliveira"
}'
```

#### Response

```json
{
  "id": "2022413e-b96f-4326-82d4-51377110c0f0",
  "name": "Lucas Oliveira",
  "email": "lucas.de.oliveira@outlook.com",
  "created_at": "2020-11-25T18:02:00.572122Z",
  "updated_at": "2020-11-25T19:33:09.381577Z"
}
```

### Delete Customer

#### Request

`DELETE /v1/customers/<id>`
```sh
curl --request DELETE \
  --url http://localhost:8000/v1/customers/2022413e-b96f-4326-82d4-51377110c0f0/ \
  --header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjA2MzM2MzY5LCJqdGkiOiIyZjVkNTI4MzRjODI0MmZmOTFkMTA3ZWJhZDUxNWYzYiIsInVzZXJfaWQiOjF9.YL_RG3m0RMepe-nEpSD6FgI6MrSwZDxYTo1OgZD-bbI'
```

#### Response

No body returned

### Create Product

#### Request

`POST v1/products/`
```sh
curl --request POST \
  --url http://localhost:8000/v1/products/ \
  --header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjA2MzM2MzY5LCJqdGkiOiIyZjVkNTI4MzRjODI0MmZmOTFkMTA3ZWJhZDUxNWYzYiIsInVzZXJfaWQiOjF9.YL_RG3m0RMepe-nEpSD6FgI6MrSwZDxYTo1OgZD-bbI' \
  --header 'Content-Type: application/json' \
  --data '{
	"id":  "571fa8cc-2ee7-5ab4-b388-06d55fd8ab2f"
}'
```

#### Response

```json
{
  "id": "571fa8cc-2ee7-5ab4-b388-06d55fd8ab2f",
  "created_at": "2020-11-25T19:38:59.819469Z",
  "updated_at": "2020-11-25T19:38:59.819487Z"
}
```

### Retrieve Product

#### Request

`GET v1/products/<id>`
```sh
curl --request GET \
  --url http://localhost:8000/v1/products/571fa8cc-2ee7-5ab4-b388-06d55fd8ab2f/ \
  --header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjA2MzM2MzY5LCJqdGkiOiIyZjVkNTI4MzRjODI0MmZmOTFkMTA3ZWJhZDUxNWYzYiIsInVzZXJfaWQiOjF9.YL_RG3m0RMepe-nEpSD6FgI6MrSwZDxYTo1OgZD-bbI'
```

#### Response

```json
{
  "id": "571fa8cc-2ee7-5ab4-b388-06d55fd8ab2f",
  "created_at": "2020-11-25T19:38:59.819469Z",
  "updated_at": "2020-11-25T19:38:59.819487Z"
}
```

### List Products


#### Request

`GET v1/products/`
```sh
curl --request GET \
  --url http://localhost:8000/v1/products/ \
  --header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjA2MzM2MzY5LCJqdGkiOiIyZjVkNTI4MzRjODI0MmZmOTFkMTA3ZWJhZDUxNWYzYiIsInVzZXJfaWQiOjF9.YL_RG3m0RMepe-nEpSD6FgI6MrSwZDxYTo1OgZD-bbI'
```

#### Response

```json
[
  {
    "id": "571fa8cc-2ee7-5ab4-b388-06d55fd8ab2f",
    "created_at": "2020-11-25T19:38:59.819469Z",
    "updated_at": "2020-11-25T19:38:59.819487Z"
  }
]
```

### Delete Product

#### Request

`DELETE v1/products/<id>`
```sh
curl --request DELETE \
  --url http://localhost:8000/v1/products/571fa8cc-2ee7-5ab4-b388-06d55fd8ab2f/ \
  --header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjA2MzM2MzY5LCJqdGkiOiIyZjVkNTI4MzRjODI0MmZmOTFkMTA3ZWJhZDUxNWYzYiIsInVzZXJfaWQiOjF9.YL_RG3m0RMepe-nEpSD6FgI6MrSwZDxYTo1OgZD-bbI'
```

#### Response

No body returned

### Create Customer Favorite

#### Request

`POST v1/customers/<id>/favorites/`
```sh
curl --request POST \
  --url http://localhost:8000/v1/customers/c4415093-c454-44fc-a958-facb1a2e39e8/favorites/ \
  --header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjA2MzM2MzY5LCJqdGkiOiIyZjVkNTI4MzRjODI0MmZmOTFkMTA3ZWJhZDUxNWYzYiIsInVzZXJfaWQiOjF9.YL_RG3m0RMepe-nEpSD6FgI6MrSwZDxYTo1OgZD-bbI' \
  --header 'Content-Type: application/json' \
  --data '{
	"id": "571fa8cc-2ee7-5ab4-b388-06d55fd8ab2f"
}'
```

#### Response

No body returned.

### List customer favorites

#### Request

`GET v1/customers/<id>/favorites/
```sh
curl --request GET \
  --url http://localhost:8000/v1/customers/c4415093-c454-44fc-a958-facb1a2e39e8/favorites/ \
  --header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjA2MzM2MzY5LCJqdGkiOiIyZjVkNTI4MzRjODI0MmZmOTFkMTA3ZWJhZDUxNWYzYiIsInVzZXJfaWQiOjF9.YL_RG3m0RMepe-nEpSD6FgI6MrSwZDxYTo1OgZD-bbI'
```

#### Response

```json
[
  {
    "id": "571fa8cc-2ee7-5ab4-b388-06d55fd8ab2f",
    "title": "Churrasqueira Elétrica Mondial 1800W",
    "price": "159.00",
    "image": "http://challenge-api.luizalabs.com/images/571fa8cc-2ee7-5ab4-b388-06d55fd8ab2f.jpg",
    "brand": "mondial",
    "reviewScore": 4.352941
  }
]
```

### Retrieve Customer Favorite

#### Request

`GET v1/customers/<customer_id>/favorites/<product_id>/`
```sh
curl --request GET \
  --url http://localhost:8000/v1/customers/c4415093-c454-44fc-a958-facb1a2e39e8/favorites/571fa8cc-2ee7-5ab4-b388-06d55fd8ab2f/ \
  --header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjA2MzM2MzY5LCJqdGkiOiIyZjVkNTI4MzRjODI0MmZmOTFkMTA3ZWJhZDUxNWYzYiIsInVzZXJfaWQiOjF9.YL_RG3m0RMepe-nEpSD6FgI6MrSwZDxYTo1OgZD-bbI'
```

#### Response

```json
{
  "id": "571fa8cc-2ee7-5ab4-b388-06d55fd8ab2f",
  "title": "Churrasqueira Elétrica Mondial 1800W",
  "price": "159.00",
  "image": "http://challenge-api.luizalabs.com/images/571fa8cc-2ee7-5ab4-b388-06d55fd8ab2f.jpg",
  "brand": "mondial",
  "reviewScore": 4.352941
}
```

### Delete Customer Favorite

#### Request

`DELETE v1/customers/<customer_id>/favorites/<product_id>`
```sh
curl --request DELETE \
  --url http://localhost:8000/v1/customers/c4415093-c454-44fc-a958-facb1a2e39e8/favorites/571fa8cc-2ee7-5ab4-b388-06d55fd8ab2f/ \
  --header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjA2MzQwMDU3LCJqdGkiOiI2Njc1ZDE3NWQzZWI0NTA5OWQ2NjQ3NWYzNTlhNmUwOSIsInVzZXJfaWQiOjF9.LYGUXbEaZpTMChR0EBphsHm9VN9nwun6oizlTnUsNJE'
```

#### Response

No body returned.
