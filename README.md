# flask-word2vec-segmenter

This is a Flask-based web application that leverages Word2Vec to perform item segmentation based on the uploaded training data.
I put this together while on a couch watching TV at 1 AM so it scales as terribly as you expect it to as the traning data size increases.

## Overview

The application uses the Word2Vec model from the Gensim library to train on uploaded CSV files and segment items based on their semantic similarity. The application provides a simple web interface for uploading training data, tuning the model, and performing segmentation.

## Features

- **User Authentication**: The application uses HTTP Basic Authentication to protect its routes. The default username and password are set to "admin" and "adminpass" respectively, but these can be overridden by setting the `APP_USER` and `APP_PASSWORD` environment variables while running locally or when using Docker.

- **File Upload**: You can upload CSV files to be used as training data for the Word2Vec model in the `Upload Data` section. The uploaded files are stored in the "uploads" directory.

- **Model Tuning**: Users can tune the parameters of the Word2Vec model through the `Tune Model` web interface. The parameters that can be tuned include the window size, minimum count, skip-gram or CBOW mode, hierarchical softmax or negative sampling, number of negative samples, number of worker threads, and the random seed.

- **Item Segmentation**: Once the model is trained, users can input a query to the GET API like `http://localhost:5000/api/alikes?query=<query>`, and the application will return a list of items that are semantically similar to the input query.

## Usage

1. Clone the repository and navigate to the project directory.
2. Install the required Python packages by running `pip install -r requirements.txt`.
3. Run the application by executing `python app.py` or `python3 app.py`.
4. Open a web browser and navigate to `http://localhost:5000`.

## Using Docker

Run the below command and you should be up and running

```
docker run -p5000:5000 ghcr.io/ash0ne/flask-word2vec-segmenter:latest
```

## License

This project is licensed under the MIT License.
