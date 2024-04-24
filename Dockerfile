FROM python:3.11-bookworm

# Install NFACT package
COPY /NFACT /NFACT
RUN pip install .

# Set up a mount point for NFACT directory
VOLUME /NFACT

# Set the working directory to the mount point
WORKDIR /NFACT

# Set the command to run a bash terminal
CMD ["/bin/bash"]
