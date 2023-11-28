docker build . --tag=robertsj32/antibody_generation_streamlit:latest

# Load environment variables from .env file
export $(grep -v '^#' .env | xargs)

# # Run docker container
docker run -e runpod_id=$runpod_id -e runpod_secret=$runpod_secret -p 8501:8501 robertsj32/antibody_generation_streamlit:latest