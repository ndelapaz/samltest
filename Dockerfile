FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt .
COPY requirements2.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install pip --upgrade
RUN pip install pyopenssl --upgrade
RUN pip install pyOpenSSL==23.1.1
# RUN pip install --no-deps --no-cache-dir -r requirements2.txt

COPY . .

# Expose the port that the application listens on.
EXPOSE 8082

# Run the application.
CMD python3 -m flask run --host=0.0.0.0 --port=8082
#RUN ["bash"]