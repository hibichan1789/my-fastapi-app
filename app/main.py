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
    weather_url = os.environ.get("WEATHERURL")
    weather_api_key = os.environ.get("WEATHERAPIKEY")
    if not zipcode_url or not geo_url or not weather_url or not weather_api_key:
        raise HTTPException(status_code=500, detail="Server error")
    try:
        async with httpx.AsyncClient() as client:
            zipcode_response = await client.get(zipcode_url, params={"zipcode": zipcode})
            zipcode_response.raise_for_status()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=502, detail=str(e))
    zipcode_json = zipcode_response.json()
    if not zipcode_json["results"]:
        raise HTTPException(status_code=404, detail=f"address not found")
    address = zipcode_json["results"][0]["address1"] + zipcode_json["results"][0]["address2"]
    try:
        async with httpx.AsyncClient() as client:
            geo_response = await client.get(geo_url, params={"q":address})
            geo_response.raise_for_status()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=502, detail=str(e))
    geo_json = geo_response.json()
    if len(geo_json) == 0:
        raise HTTPException(status_code=404, detail="coordinates not found")
    coordinates = geo_json[0]["geometry"]["coordinates"]
    latitude = round(coordinates[1], 4)
    longitude = round(coordinates[0], 4)

    #天気情報の取得
    weather_params = {
        "lat": latitude,
        "lon": longitude,
        "appid": weather_api_key,
        "units": "metric",
        "lang": "ja"
    }
    try:
        async with httpx.AsyncClient() as client:
            weather_response = await client.get(weather_url, params=weather_params)
            weather_response.raise_for_status()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=502, detail=str(e))
    weather_json = weather_response.json()
    weather_description = weather_json["weather"][0]["description"]
    weather_temperature = weather_json["main"]["temp"]
    weather_humidity = weather_json["main"]["humidity"]
    result = {
        "zipcode": zipcode,
        "address": address,
        "coordinate":[
            latitude, longitude
        ],
        "weather_info":{
            "description": weather_description,
            "temperature": weather_temperature,
            "humidity": weather_humidity
        }
    }
    return result