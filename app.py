from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, Response
import pandas as pd
import joblib

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Load models
model1 = joblib.load("model_diag.pkl")
model2 = joblib.load("model_sev.pkl")
encoders = joblib.load("encoders.pkl")
columns = joblib.load("columns.pkl")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@app.head("/")
def health_check():
    return Response(status_code=200)

@app.post("/predict")
async def predict(request: Request):
    data = await request.json()
    df = pd.DataFrame([data])

    for col in df.columns:
        if col in encoders:
            le = encoders[col]
            if df[col].iloc[0] in le.classes_:
                df[col] = le.transform(df[col])
            else:
                df[col] = 0

    df = df[columns]

    d = model1.predict(df)[0]
    s = model2.predict(df)[0]

    d = str(encoders["Diagnosis"].inverse_transform([d])[0])
    s = str(encoders["Severity"].inverse_transform([s])[0])

    prob = float(model1.predict_proba(df)[0].max())

    return {
        "Diagnosis": d,
        "Severity": s,
        "Confidence": round(prob * 100, 2)
    }
