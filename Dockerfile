# Start by pulling the python image
FROM python:3.8-alpine

# Copy the requirements file into the image
COPY requirements.txt /app/requirements.txt

# Switch to the workdir
WORKDIR /app

# Install the dependancies and packages in the requirements file
RUN pip install --no-cache-dir -r requirements.txt

# Copy every content from the local file to the image
COPY . /app

# Configure the container to run in an executed manner
ENTRYPOINT [ "python" ]

CMD [ "app.py" ]
