# Travel App API
---

### Main Features

* **User Management**

  * User registration with password hashing
  * Login and authentication with access control
  * User status (`is_fired`) to restrict access
* **Project Management**

  * Create, read, update, delete travel projects (with all conditions)
* **Place Management**

  * Add places to projects
  * Update place details and mark as visited
  * Limit on number of places per project
* **Security**

  * Password hashing
  * Basic authentication for API endpoints
  * Restricted access to authorized users only
* **External API Integration**

  * Places validated against third-party API
  * Responses cached and validated for efficiency
* **Error Handling & Logging**

  * Centralized error handler with proper HTTP responses
  * Logging of all requests and exceptions

---

## Setup

### Prerequisites

* Docker
* Docker Compose

### Build the Docker and run locally:
```
docker-compose up --build
```
### The API will be available at: 
```
http://localhost:8000
```
### To see live logs in console:
```
docker logs -f <container_id>
```
##### or use `logs/requests/errors.log` to see the logs history (file will automaticly be created)
---
# `Important`
### To have an access to endpoints, first of all you need to create a user in `/register` endpoint. 
### Then use SwaggerUI Authorization button to login

---

## API Documentation

The API provides an **OpenAPI/Swagger UI** available at:

```
http://localhost:8000/docs
```

* All endpoints require authentication via Basic Auth except for `login` and `register`.
* Successful login will return user details in a structured JSON format.
* Error responses are standardized via the centralized error handler.

---

## Using Postman Collection

Open **Postman → Import → File → postman_col.json**

---

## Notes

* Maximum 10 places per project.
* All exceptions are handled and logged via the centralized error handler.
* SQLite database file: `travel_app.db` (will automaticly be created with all tables)
* Python version: 3.11
