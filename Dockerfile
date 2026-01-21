FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y \
  curl \
  gnupg \
  unixodbc \
  unixodbc-dev \
  ca-certificates \
  && rm -rf /var/lib/apt/lists/*

RUN curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o /usr/share/keyrings/microsoft-prod.gpg \
  && curl https://packages.microsoft.com/config/debian/12/prod.list > /etc/apt/sources.list.d/mssql-release.list \
  && apt-get update \
  && ACCEPT_EULA=Y apt-get install -y msodbcsql18 \
  && ACCEPT_EULA=Y apt-get install -y mssql-tools18 \
  && echo 'export PATH="$PATH:/opt/mssql-tools18/bin"' >> ~/.bashrc \
  && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
COPY app.py .
COPY src/ ./src/

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV DB_DRIVER="{ODBC Driver 18 for SQL Server}"

ENV PYTHONPATH=/app
ENV FLASK_ENV=production

EXPOSE 5000

CMD ["python", "app.py"]
