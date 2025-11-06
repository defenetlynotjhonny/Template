FROM python:3.14

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE=1  
ENV PYTHONUNBUFFERED=1     

RUN mkdir /app
RUN cd /app
# Set the working directory inside the container
WORKDIR /app

# Install Python dependencies
# Copying requirements first leverages Docker's build cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project code into the container
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Run the Django development server
# This is great for development, but not for production

CMD ["python", "xrpl_platform/manage.py", "runserver", "0.0.0.0:8000"]