# Build the image
# docker build .

# Run the image
docker run --expose 8080 --gpus all -e READER_MODEL_PATH=deepset/roberta-base-squad2 -d entroprediction:latest