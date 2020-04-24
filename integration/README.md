product_catalogue.csv is intentionally excluded from this directory.

It can be downloaded here (with permission only):
https://drive.google.com/open?id=1reg70l9NnSJSDM8VAValvojyhizn2yLO

### API Usage

API is being hosted on Linode (Linux server)

Address is on `http://139.162.62.89:5000/`

##### Skin Care Advisor

POST request to `http://139.162.62.89:5000/sca`

Body of request contains the following JSON:
```
{
        "age": 21,
        "skin_type": "normal",
        "allergies": null,
        "price": null,
        "concerns": ["acne", "dark_eye", "oiliness"],
        "preferences": null,
        "image": "insert base64 string encoding of image here"
}
```

Returns a JSON response of scores, recommendations, image links, etc.

##### Retrieve cropped images

GET request, follow link received from above SCA request

Returns an image file

