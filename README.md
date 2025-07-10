# AvoMD Assignment Backend
This project is a practical backend assignment using Django, Celery, OpenAI, drf-yasg, Docker, and Nginx.

## AI Usage Summary
I designed the architecture and business logic independently, and used AI to review my plans for blind spots and to accelerate implementation of structured components like viewsets, serializers, and Celery task functions. While the core logic was simple, development speed was critical, so I let AI generate portions of the code—but always with caution.

All AI-generated code was manually reviewed and tested. I verified that asynchronous GPT calls and subsequent DB updates worked reliably within Celery tasks. More importantly, I did not rely on AI to catch implicit security risks. For instance, the Redis configuration provided by GPT omitted password protection, exposing the system to unauthenticated access. I recognized this risk and corrected it by explicitly enforcing authentication.

Rather than treating AI as a black box, I used it as a second set of hands—efficient, but not trustworthy on its own. This freed up more time to focus on validation, exception handling, and modeling for long-term scalability and safety.

Every line of critical logic passed through my eyes. The final result reflects my decisions, with AI accelerating—but never replacing—my responsibility.

## Description
- **Django** enqueues Celery tasks for job creation; Celery Worker fetches tasks from Redis broker.
- **Nginx** and **Gunicorn** run together in front of Django within the same container, handling HTTP requests and serving as a reverse proxy and WSGI server, respectively.
- **Redis** runs as a separate container and is used as the message broker for Celery, enabling asynchronous task queuing and communication between Django and Celery workers.
- **Celery Worker** reads scheduled task information from Redis, reads/writes jobs in the DB, and calls the OpenAI API, saving results back to the DB. It runs as a separate background task from the Django API, enabling asynchronous processing of OpenAI API calls. This design prevents Django threads from being blocked by I/O delays and allows heavy or slow operations to be handled efficiently in the background. Although true async OpenAI API calls were not possible due to interference with the synchronous Django ORM, separating the workload from the Django server with Celery still provides significant performance benefits by offloading slow operations from the main web process.
- **PostgreSQL** runs as a separate container and is used as the main database for all persistent data.
- All services run as separate Docker containers.

## How to Run
- To run the service, navigate to the root directory of the project.
- Copy the .env file received by email into the project’s root directory.
- Run the following command: docker compose up
- This command also automatically runs the tests when executed.
- Once it's running, you can access the service at http://localhost:80.
- API documentation is available at:
    - Swagger UI: http://localhost/swagger/
    - Redoc: http://localhost/redoc/
    - OpenAPI JSON: http://localhost/openapi.json

## License

This project is licensed under the [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0).