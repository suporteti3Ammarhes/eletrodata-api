FROM python:3.13-slim

WORKDIR /app

# Primeiro instale as dependências do sistema
RUN apt-get update && apt-get install -y \
  curl \
  gnupg \
  unixodbc \
  unixodbc-dev \
  ca-certificates \
  build-essential \
  gcc \
  g++ \
  && rm -rf /var/lib/apt/lists/*

RUN curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o /usr/share/keyrings/microsoft-prod.gpg \
  && curl https://packages.microsoft.com/config/debian/12/prod.list > /etc/apt/sources.list.d/mssql-release.list \
  && apt-get update \
  && ACCEPT_EULA=Y apt-get install -y msodbcsql18 \
  && ACCEPT_EULA=Y apt-get install -y mssql-tools18 \
  && echo 'export PATH="$PATH:/opt/mssql-tools18/bin"' >> ~/.bashrc \
  && rm -rf /var/lib/apt/lists/*

# Agora copie e instale requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Por último, copie o código
COPY app.py .
COPY src/ ./src/

ENV DB_DRIVER="{ODBC Driver 18 for SQL Server}"
ENV PYTHONPATH=/src
ENV FLASK_ENV=production

EXPOSE 5000

CMD ["python", "app.py"]