# AntibodyGPT:  Docker Streamlit Antibody Protein Generation Application

This repository contains a Streamlit application for antibody protein generation, packaged with Docker for easy setup and deployment.


## AntibodyGPT: A Fine-Tuned GPT for De Novo Therapeutic Antibodies

- [Web Demo](https://orca-app-ygzbp.ondigitalocean.app/Demo_Antibody_Generator)
- [Huggingface Model Repository](https://huggingface.co/AntibodyGeneration)

Antibodies are proteins that bind to a target protein (called an antigen) in order to mount an immune response. 
They are incredibly **safe** and **effective** therapeutics against infectious diseases, cancer, and autoimmune disorders.

Current antibody discovery methods require a lot of capital, expertise, and luck. Generative AI opens up the possibility of 
moving from a paradigm of antibody discovery to antibody generation. However, work is required to translate the advances of LLMs to the realm of drug discovery.

AntibodyGPT is a fine-tuned GPT language model that researchers can use to rapidly generate functional, diverse antibodies for any given target sequence

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Docker: The application is containerized with Docker, so you'll need Docker installed on your machine. You can download Docker [here](https://www.docker.com/products/docker-desktop).

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/joethequant/docker_streamlit_antibody_protein_generation.git
    ```

2. Navigate to the project directory:
    ```bash
    cd docker_streamlit_antibody_protein_generation
    ```

3. Build and run the Docker image:
    ```bash
    build_and_run.sh
    ```
    The application should now be running at `http://localhost:8501`.

4. Build and push to dockerhub: Edit contents to your location.
    ```bash
    build_and_push.sh
    ```
5. This app uses a serverless api pushed to runpod. You must set these env variables in a .env file.
- runpod_id
- runpod_secret

6. The serverless api docker code is located here: 
- Github: [https://github.com/joethequant/docker_protein_generator](https://github.com/joethequant/docker_protein_generator)
- Public Image: [https://hub.docker.com/repository/docker/robertsj32/antibody_generation_runpod/general](https://hub.docker.com/repository/docker/robertsj32/antibody_generation_runpod/general)


## Usage

Provide instructions on how to use your application here.

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.