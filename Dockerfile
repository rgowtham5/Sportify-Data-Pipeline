# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Set environment variables
ENV SPOTIPY_CLIENT_ID=<b0ad7e3196664e03af1ce3c52f88033b>
ENV SPOTIPY_CLIENT_SECRET=<c1a7d4d0fc714204bedee9f671f73d99>
ENV SPOTIPY_REDIRECT_URI=<http://localhost:3000/callback>

# Define the command to run your script
CMD ["python", "spotify_artist_insights_taylor_swift.py"]