FROM python:3.10-slim

# Set the default directory where CMD will execute
WORKDIR /app

# Install dependencies from requirements file
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
ENV PYTHONUNBUFFERED=1


EXPOSE 5000

CMD ["python","-u","monitor.py"]

