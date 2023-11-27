FROM python:3.8-slim

WORKDIR /app
ADD . /app

RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["python", "src/scraper.py",
    "--configs", "/app/config/configs",
    "--push-config", "/app/config/push_config.json"
]