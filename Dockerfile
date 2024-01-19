FROM python:3.11

# Install Poetry
RUN pip install poetry

# Set the working directory to /app
WORKDIR /app

# Copy only the pyproject.toml and poetry.lock to leverage Docker caching
COPY pyproject.toml poetry.lock /app/

# Install project dependencies
RUN poetry install --no-dev

# Copy the rest of the application code
COPY . /app/

# Run app.py when the container launches
CMD ["poetry", "run", "python", "app.py"]
