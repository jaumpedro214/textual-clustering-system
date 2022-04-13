FROM continuumio/miniconda3
WORKDIR /code
COPY . .
RUN echo "Conda activated"
RUN cat req_environment.yaml
RUN conda env create -f req_environment.yaml
SHELL ["conda", "run", "-n", "train", "/bin/bash", "-c"]
RUN python train.py
ENTRYPOINT ["tail", "-f", "/dev/null"]