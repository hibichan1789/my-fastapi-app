from fastapi import FastAPI
import os
app = FastAPI()

@app.get("/")
def get_root():
    test_value = os.environ.get("TEST_VALUE")
    return{"messages": "動作確認", "test_value": test_value}