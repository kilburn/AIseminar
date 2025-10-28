FROM qdrant/qdrant:v1.7.4

# Install curl for healthcheck and clean up apt cache
RUN apt-get update \
 && apt-get install -y --no-install-recommends curl ca-certificates \
 && rm -rf /var/lib/apt/lists/*
