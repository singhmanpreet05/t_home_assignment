# Dockerfile References: https://docs.docker.com/engine/reference/builder/

# Ideally use alpine image but for ease of development using the regular one
FROM python:3.9

# The latest alpine images don't have some tools like (`git` and `bash`).
# Adding git, bash and openssh to the image
#RUN apk update && apk upgrade && \
#    apk add --no-cache bash git openssh

# Make dir app
RUN mkdir /app
WORKDIR /app
COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

# Copy the source from the current directory to the Working Directory inside the container
ADD src src/

ENV PYTHONPATH="$PYTHONPATH:/app"
RUN export PYTHONPATH="$PYTHONPATH:/app"
ENV PYTHONUNBUFFERED=0

# Expose port 8000 to the outside world
EXPOSE 8000

# Run the executable
CMD ["python3", "src/main.py", "0.0.0.0", "8000"]