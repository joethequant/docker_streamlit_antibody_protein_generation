# Use an official Python runtime as a parent image
# FROM continuumio/miniconda3

FROM python:3.11


# Set the working directory in the container to /app
WORKDIR /app

# linux update and remove temp files
RUN apt-get update \
    && rm -rf /var/lib/apt/lists/*

# install miniconda
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh && \
    bash Miniconda3-latest-Linux-x86_64.sh -b -p /miniconda && \
    rm Miniconda3-latest-Linux-x86_64.sh

# Add Miniconda to PATH
ENV PATH="/miniconda/bin:${PATH}"


# #################### Install ANARCI ####################
# # download ANARCI into ANARCI folder then install ANARCI environment and install dependencies
# RUN conda create --name anarci python=3.11 -y && \
#     echo "source activate anarci" > ~/.bashrc

# # Clone ANARCI repository
# RUN git clone https://github.com/joethequant/ANARCI.git

# # Change working directory to ANARCI
# WORKDIR /app/ANARCI

# # Install ANARCI and its dependencies
# RUN /bin/bash -c "conda install ipykernel -y && \
#     python -m ipykernel install --user --name=anarci --display-name='anarci' && \
#     conda install -c conda-forge openmm pdbfixer -y && \
#     conda install -c bioconda hmmer=3.3.2 biopython -y && \
#     python setup.py install"

# # Set environment variables
# ENV PATH /opt/conda/envs/anarci/bin:$PATH
# ENV CONDA_DEFAULT_ENV anarci

# ################# END ANARCI Install ###################


# #################### Install ANARCI ####################
# # Clone ANARCI repository
# RUN git clone https://github.com/joethequant/ANARCI.git

# # Change working directory to ANARCI
# WORKDIR /app/ANARCI

# # Install ANARCI and its dependencies
# RUN /bin/bash -c "conda install ipykernel -y && \
#     python -m ipykernel install --user --display-name='Python (base)' && \
#     conda install -c conda-forge openmm pdbfixer -y && \
#     conda install -c bioconda hmmer=3.3.2 biopython -y && \
#     python setup.py install"

# ################# END ANARCI Install ###################


#################### Install ANARCI ####################
# Clone ANARCI repository
RUN git clone https://github.com/joethequant/ANARCI.git

# Change working directory to ANARCI
WORKDIR /app/ANARCI

# Install ANARCI and its dependencies
# RUN /bin/bash -c "conda install -c conda-forge openmm pdbfixer -y && \
#     conda install -c bioconda hmmer=3.3.2 biopython -y && \
#     python setup.py install"

RUN /bin/bash -c "conda install -c conda-forge openmm pdbfixer -y"
RUN /bin/bash -c "conda install -c bioconda hmmer=3.3.2 biopython -y"
RUN /bin/bash -c "python setup.py install"

################# END ANARCI Install ###################

# Change working directory to /app
WORKDIR /app

# Copy requirements file to /app
COPY requirements.txt /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# User -> must create a user to bypass permission issues on huggingface
RUN useradd -m -u 1000 user
USER user
ENV HOME /home/user
ENV PATH $HOME/.local/bin:$PATH

# Set the working directory to $HOME/app
WORKDIR $HOME
RUN mkdir app
WORKDIR $HOME/app

COPY Home.py $HOME/app
COPY sidebar.py $HOME/app
COPY logo.png $HOME/app

COPY pages $HOME/app/pages


# Make port 8501 available to the world outside this container
EXPOSE 8501

# Run app.py when the container launches
CMD streamlit run Home.py \
    --server.headless true \
    --server.enableCORS false \
    --server.enableXsrfProtection false \
    --server.fileWatcherType none \
    --browser.gatherUsageStats false
