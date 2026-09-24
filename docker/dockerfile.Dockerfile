# Specify the existing image we want to start from. It will spin up an existing
# image with ubuntu + python.
FROM python:3.14-slim

# Sets the working directory in the image we have just created
WORKDIR /app

# Invoke a shell in the image -> run the command below.
COPY requirements.txt .

RUN pip install -no-cache-dir -r requirements.txt


# Copy all the project files into the App folder?
COPY . .

# Mirrors ENTRYPOINT -> This command will run when the container starts (not at build time)
CMD ["python", "src/main.py"]
#ENTRYPOINT is a fixed executable, CMS is a default 