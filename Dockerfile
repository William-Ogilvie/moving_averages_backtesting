# Micro mamba environment with Ubuntu OS
FROM mambaorg/micromamba:ubuntu22.04

# In case ever have multiple environments
ARG ENV_FILE=environment.yml

# chown sets the owner of the copied files to the mamba user not the root user
COPY --chown=$MAMBA_USER:$MAMBA_USER $ENV_FILE /tmp/$ENV_FILE

# Create the environment and clean up
RUN micromamba install -y -n base -f /tmp/$ENV_FILE && \
    micromamba clean --all --yes

# Set as working directory
WORKDIR /app

# To build the docker image run
# docker build -t ma-backtest --build-arg ENV_FILE=environment.yml .

# When you run the container we want to bind mount the current directory to it
# docker run -it --rm --mount type=bind,src="$(pwd)",dst=/app ma-backtest