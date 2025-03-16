FROM python:3.10

WORKDIR /app

# copy files to /app
COPY . /app

# copy requirements file and install dependencies
RUN pip install -r requirements.txt && pip install -e .

# expose port app runs on
EXPOSE 8080

# Run command
CMD ["gunicorn", "-b", ":8080", "--workers", "1", "--threads", "1", "app:app", "--timeout", "3600"]
