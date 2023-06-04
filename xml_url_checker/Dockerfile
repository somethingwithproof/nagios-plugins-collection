# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run test_xml_url_checker.py when the container launches
CMD ["python", "test_xml_url_checker.py"]

# Then run xml_url_checker.py
CMD ["python", "test_xml_url_checker.py"]
