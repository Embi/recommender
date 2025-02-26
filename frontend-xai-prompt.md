# Frontend  prompt
Write a simple vue.js frontend app that satisfy the following.

## App description

It is a frontend for a simple car recommendation system.

## API:
the app communicates with a backend API available on
`http://<BASE_URL>/api/v1/`

## Authentication:
- All API calls (except `api/v1/token/fake-token`, that serves for obtaining the
  token) need to have `Authorization: Bearer <token>` header.
- Upon landing, user is required to first log-in. The log-in is done by user
  providing an email (no password). The email is then exchanged for a JWT
  Bearer token by calling `POST http://<BASE_URL>/api/v1/token/fake-token` with
  `{"emai": "<user-email>"}` request body
- After log-in, user is redirected to the main app page

## Main App page

The main app page has two sections:

1. Allows to exectute search queries.
2. Shows recommended cars for the user.

### 1. Search queries

Search allows user to specify following query parameters:

- brand
- min_year
- max_year
- min_price
- max_price
- fuel

The search query is then executed calling this endpoint `GET /api/v1/cars/search`.
An example query would look like this:

`GET /api/v1/cars/search?brand=Skoda&min_year=2013&max_year=2015`

An example result returned by the endpoint would look like this:

```json
{
  "listings": [
    {
      "id": 82,
      "brand": "Skoda",
      "name": "Skoda Rapid 1.5 TDI Elegance",
      "selling_price": 450000
    },
    {
      "id": 181,
      "brand": "Skoda",
      "name": "Skoda Rapid 1.6 MPI Ambition With Alloy Wheel",
      "selling_price": 640000
    },
    {
      "id": 681,
      "brand": "Skoda",
      "name": "Skoda Rapid 1.6 MPI AT Elegance Plus",
      "selling_price": 600000
    },
    {
      "id": 729,
      "brand": "Skoda",
      "name": "Skoda Superb 1.8 TSI",
      "selling_price": 599000
    }
  ]
}
```

The app should than show the results in some paged manner (let's say 10 per
page). User should be able to click on each of the results to display details
about a particular listing.

### 2. User recommendations section

Recommendations for a logged-in user can be obtained by calling
`GET /api/v1/cars/recommendations`.
An example response looks like this:

```json
{
  "recommended": [
    {
      "id": 1,
      "brand": "Maruti",
      "name": "Maruti 800 AC",
      "selling_price": 60000
    },
    {
      "id": 4845,
      "brand": "Ford",
      "name": "Ford Ecosport 1.5 DV5 MT Titanium",
      "selling_price": 750000
    },
    {
      "id": 3561,
      "brand": "Mahindra",
      "name": "Mahindra XUV500 W8 4WD",
      "selling_price": 625000
    }
  ]
}
```

The recommendation section should display first 10 recommended listings from
the list. User should be able to click on each of the recommended listings to
obtain details about the listing.


## Listing details

When user click on a listing (either recommended or search) the listing detail
page will be showed. The listing details can be obtained by calling
`GET /api/v1/cars/detail/<listing_id>` API endpoint.
An example response looks like this:


```json
{
  "brand": "Maruti",
  "name": "Maruti 800 AC",
  "year": 2007,
  "selling_price": 60000,
  "km_driven": 70000,
  "fuel": "Petrol",
  "seller_type": "Individual",
  "transmission": "Manual",
  "owner": "First Owner"
}
```
