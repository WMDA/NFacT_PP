FROM python:3.11-bookworm

# Install NFACT package
COPY . /NFACT

# Set up a mount point for NFACT directory
VOLUME /NFACT

# Set the working directory to the mount point
WORKDIR /NFACT
RUN pip install .
# Set the command to run a bash terminal
CMD ["/bin/bash"]
