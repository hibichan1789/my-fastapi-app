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
    if not zipcode_url:
        raise HTTPException(status_code=500, detail="Server error")
    try:
        async with httpx.AsyncClient() as client:
            zipcode_response = await client.get(zipcode_url, params={"zipcode": zipcode})
            zipcode_response.raise_for_status()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=502)
    zipcode_json = zipcode_response.json()
    return zipcode_json