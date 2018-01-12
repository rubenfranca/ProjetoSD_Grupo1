# Use an official Python runtime as a parent image
FROM python:2.7-slim


# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt


# Make ports available to the world outside this container
EXPOSE 4003
EXPOSE 8000
EXPOSE 4002
EXPOSE 4001

# Define environment variable
ENV NAME World

# Descomentar o codigo para o container a fazer build
#CMD ["python", "routes.py"]
#CMD ["python", "salas.py"]
#CMD ["python", "reservas.py"]
#CMD ["python", "grpcserver.py"]