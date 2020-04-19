product_catalogue.csv is intentionally excluded from this directory.

It can be downloaded here (with permission only):
https://drive.google.com/open?id=1reg70l9NnSJSDM8VAValvojyhizn2yLO

### API Usage

Run API locally by `python application.py`

Address is on `http://localhost:5000`

##### Skin Care Advisor

POST request to `http://localhost:5000/sca`

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

Returns a JSON response as following:

```
{
    statusCode: 200,
    body: {
        "identifier": 17733369882703254762,
        "acne_ch": 0.010000000000000009,
        "acne_fh": -0.0040000000000000036,
        "acne_lc": 0.3680000000000001,
        "acne_overall": 0.096,
        "acne_rc": 0.008000000000000007,
        "acne_recommendation": "{...}"
    }
}
```

##### Retrieve cropped images

POST request to `http://localhost:5000/image`

Body of request contains the following JSON:
```
{
	"identifier": 17733369882703254762,
	"type": "crows_feet_l"
}
```

Replace key `type` with image type e.g. `"full_image"`, 
`"wrinkles_lbe_image"`

Returns a JSON response as following:
```
{
    statusCode: 200,
    image: "base64 encoding of image"
}
```