# Dockerfile for the image processing service
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY ./requirements.txt /app/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt
RUN pip install python-multipart

# Copy the application code
COPY ./main.py /app/main.py
COPY ./model_segformer_classes.json /app/model_segformer_classes.json
COPY ./model_segformer.pth /app/model_segformer.pth

# Expose the port the app runs on
EXPOSE 8001

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]