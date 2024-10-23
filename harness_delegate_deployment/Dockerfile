FROM harness/delegate:24.09.83909@sha256:79967d8e2ace31414f8370aae069b19020b218c30c8c7e28ee4e21548b1457de

USER root

# Install required packages
RUN microdnf install curl tar python3 unzip gcc glibc-devel libffi-devel openssl openssl-devel && \
    microdnf clean all

# Create symbolic link for Python3
RUN ln -s /usr/bin/python3 /usr/bin/python

# Install Liquibase
RUN mkdir -p /usr/local/liquibase && \
    curl -L https://github.com/liquibase/liquibase/releases/download/v4.29.2/liquibase-4.29.2.zip -o liquibase.zip && \
    unzip liquibase.zip -d /usr/local/liquibase && \
    rm liquibase.zip

# Create the directory for Liquibase extensions
RUN mkdir -p /usr/local/liquibase/lib

# Download the Liquibase No ChangeLog Lock extension and place it in the Liquibase lib directory
RUN curl -L https://github.com/liquibase/liquibase-nochangeloglock/releases/download/v4.29.2/liquibase-nochangeloglock-4.29.2.jar \
  -o /usr/local/liquibase/lib/liquibase-nochangeloglock-4.29.2.jar

# Set the CLASSPATH environment variable to include the JDBC driver and the No ChangeLog Lock extension
ENV CLASSPATH="/usr/local/lib/snowflake-jdbc.jar:/usr/local/liquibase/lib/liquibase-nochangeloglock-4.29.2.jar"

# Set the PATH environment variable to include Liquibase binaries
ENV PATH="/usr/local/liquibase:$PATH"

# Install Python packages: Snowflake connector, dotenv, and PyYAML
RUN pip3 install --upgrade pip && \
    pip3 install snowflake-connector-python python-dotenv PyYAML

# Download the Snowflake JDBC driver
RUN curl -L https://repo1.maven.org/maven2/net/snowflake/snowflake-jdbc/3.13.22/snowflake-jdbc-3.13.22.jar -o /usr/local/lib/snowflake-jdbc.jar

# Copy the start script into the container
COPY start.sh /usr/local/bin/start.sh
RUN chmod +x /usr/local/bin/start.sh

# Default command
CMD ["/usr/local/bin/start.sh"]
