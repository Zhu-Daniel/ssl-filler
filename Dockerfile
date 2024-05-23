# syntax=docker/dockerfile:1

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/go/dockerfile-reference/

# Want to help us make this template better? Share your feedback here: https://forms.gle/ybq9Krt8jtBL3iCk7

ARG PYTHON_VERSION=3.12.2
FROM python:${PYTHON_VERSION}-slim as base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1
# ENV FILE_PATH="SSLSheets"
# ENV FILE="Tacy_Foundation_SSL_Hours_041324.xlsx"
# ENV SHEET="Form Responses 1"
# ENV MONTGOMERY_SSL="SSLForms/montgomerySSLsigned.pdf"
# ENV SSL_PATH="FilledSSL"
# ENV LOGS_PATH="SSLEventLogs"

WORKDIR /app



# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/go/dockerfile-user-best-practices/
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
# Leverage a bind mount to requirements.txt to avoid having to copy them into
# into this layer.
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt


# Switch to the non-privileged user to run the application.
USER appuser

# Copy the source code into the container.
COPY . .

# Before continuing, use root to give it permission to create files in FilledSSL and SSLEventLogs
USER root
RUN ls -al | echo
RUN chown -R appuser:appuser FilledSSL
RUN chown -R appuser:appuser SSLEventLogs
RUN chown -R appuser:appuser SSLSheets

# Switch to the non-privileged user to run the application.
USER appuser

RUN pwd && ls && echo "print paths"
RUN echo $(ls -1)
RUN echo $(pwd)

# Expose the port that the application listens on.
EXPOSE 8000

# Run the application.
# CMD python sslPDF.py

CMD python sslPDF.py