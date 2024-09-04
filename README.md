# healthcare_test_task

1. docker compose build api
2. docker compose up api 

in second terminal 
1. docker exec -it api bash
2. alembic upgrade head

open in browser http://0.0.0.0:8000/docs
endpoint with method POST to save HL7 AD01 message