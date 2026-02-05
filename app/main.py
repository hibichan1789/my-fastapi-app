from fastapi import FastAPI, Path, HTTPException
import os
import httpx

app = FastAPI()
@app.get("/")
def get_root():
    test_value = os.environ.get("TEST_VALUE")
    return{"messages": "動作確認", "test_value": test_value}

@app.get("/weather/{zipcode}")
async def get_current_weather(zipcode:str=Path(..., pattern=r"^\d{7}$")):
    zipcode_url = os.environ.get("ZIPCODEURL")
    geo_url = os.environ.get("GEOURL")
    if not zipcode_url or not geo_url:
        raise HTTPException(status_code=500, detail="Server error")
    try:
        async with httpx.AsyncClient() as client:
            zipcode_response = await client.get(zipcode_url, params={"zipcode": zipcode})
            zipcode_response.raise_for_status()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=502, detail=e)
    zipcode_json = zipcode_response.json()
    address = zipcode_json["results"][0]["address1"] + zipcode_json["results"][0]["address2"]
    if not address:
        raise HTTPException(status_code=404, detail=f"address not found")
    try:
        async with httpx.AsyncClient() as client:
            geo_response = await client.get(geo_url, params={"q":address})
            geo_response.raise_for_status()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=502, detail=e)
    geo_json = geo_response.json()
    if len(geo_json) == 0:
        raise HTTPException(status_code=404, detail="coordinates not found")
    coordinates = geo_json[0]["geometry"]["coordinates"]
    latitude = coordinates[1]
    longitude = coordinates[0]
    return {
        "address": address,
        "latitude":latitude,
        "longitude": longitude
    }