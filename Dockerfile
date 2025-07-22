FROM python:3.13

# Create the app directory
RUN mkdir /app
 
# Set the working directory inside the container
WORKDIR /app

# Set environment variables 
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 

# Upgrade pip and install dependencies
COPY ./requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project code
COPY ./core /app/

# Copy entrypoint script
#COPY ./entrypoint.sh /app/
# RUN chmod +x /app/entrypoint.sh

# Expose the Django port
EXPOSE 8000

# Use custom entrypoint
#ENTRYPOINT ["/app/entrypoint.sh"]
