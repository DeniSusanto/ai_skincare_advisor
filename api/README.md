## API usage

Run `python application.py` on console. Server will run on `localhost:5000`.

# Scoring API

Send POST request to `http://localhost:5000/score` with the key `image` and value of the image as a base64 string.

# Recommendation API

POST request to `http://localhost:5000/recommendation` with a JSON input, same format as `main_input` of recommendation system.