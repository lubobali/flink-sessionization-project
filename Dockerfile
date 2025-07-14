FROM apache/flink:1.16.2-scala_2.12

USER root

# Install dependencies + Python 3.8 + pip
RUN apt-get update && \
    apt-get install -y software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y curl openjdk-8-jdk python3.8 python3.8-dev python3-pip && \
    ln -sf /usr/bin/python3.8 /usr/bin/python && \
    pip install --upgrade pip setuptools wheel

# Set JAVA_HOME for pemja
ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
ENV PATH="$JAVA_HOME/bin:$PATH"

# Clean old Flink pip installs (just in case)
RUN pip uninstall -y apache-flink apache-flink-libraries || true

# Set working directory
WORKDIR /opt/src

# Copy requirements.txt
COPY requirements.txt .

# Install Python dependencies (including pyflink==1.0)
RUN pip install --no-cache-dir -r requirements.txt

# Add Flink connector JARs
RUN mkdir -p /opt/flink/lib/
COPY ./lib/*.jar /opt/flink/lib/

# Copy source code
COPY ./src /opt/src/
