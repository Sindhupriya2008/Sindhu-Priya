🔹 Project Overview

A Student Finance Manager Web App that helps students manage their expenses, predict future spending, set financial goals, and receive alerts when they’re close to exceeding their budget.

Core Features

Automated Expense Categorization

Input: Expense data (manual entry or uploaded bank statements/CSV).

AI model (NLP / ML): Classify expenses into categories (Food, Rent, Travel, Entertainment, etc.).

Predictive Spending Analysis

Train a simple time series model (ARIMA, LSTM, or Prophet) on past expenses.

Forecast next month’s expenses.

Show trends in charts.

Goal Tracking
Users set savings/spending goals (e.g., "Save $200 this month").

Track progress toward goals in real-time.

Budget Alerts

Notify students when they are nearing their monthly budget limit.

Example: Send email or dashboard alert when 80% of budget is spent.

Predictive Analytics Dashboard

Graphs & charts showing:

Spending by category (Pie chart)

Monthly trends (Line chart)

Predicted vs. actual spending (Bar/Line chart)


#python
from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
from sklearn.linear_model import LinearRegression
import random

app = FastAPI()

# In-memory storage (replace with DB in production)
expenses = []

class Expense(BaseModel):
    description: str
    amount: float

@app.post("/add_expense")
def add_expense(exp: Expense):
    # Simple rule-based categorization (can replace with ML)
    if "food" in exp.description.lower():
        category = "Food"
    elif "rent" in exp.description.lower():
        category = "Housing"
    elif "travel" in exp.description.lower():
        category = "Transport"
    else:
        category = "Other"
    
    expenses.append({"desc": exp.description, "amount": exp.amount, "category": category})
    return {"msg": "Expense added", "category": category}

@app.get("/predict_spending")
def predict_spending():
    if len(expenses) < 2:
        return {"msg": "Not enough data"}
    
    df = pd.DataFrame(expenses)
    df["index"] = range(len(df))
    
    model = LinearRegression()
    model.fit(df[["index"]], df["amount"])
    
    future = model.predict([[len(df)+1]])[0]
    return {"predicted_next_expense": round(float(future), 2)}

   #HTML
    import { useState, useEffect } from "react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip } from "recharts";

export default function App() {
  const [expenses, setExpenses] = useState([]);
  const [desc, setDesc] = useState("");
  const [amount, setAmount] = useState("");
  const [prediction, setPrediction] = useState(null);

  const addExpense = async () => {
    const res = await fetch("http://127.0.0.1:8000/add_expense", {
      method: "POST",
            headers: {"Content-Type": "application/json"},
      body: JSON.stringify({ description: desc, amount: parseFloat(amount) })
    });
    const data = await res.json();
    alert("Expense categorized as " + data.category);
  };

  const getPrediction = async () => {
    const res = await fetch("http://127.0.0.1:8000/predict_spending");
    const data = await res.json();
    setPrediction(data.predicted_next_expense);
  };

 return (
    <div className="p-6 max-w-lg mx-auto">
      <h1 className="text-2xl font-bold mb-4">Student Finance Manager</h1>
      
      <input className="border p-2 mr-2" placeholder="Description" onChange={e => setDesc(e.target.value)} />
      <input className="border p-2 mr-2" type="number" placeholder="Amount" onChange={e => setAmount(e.target.value)} />
      <button className="bg-blue-500 text-white px-4 py-2 rounded" onClick={addExpense}>Add</button>

      <div className="mt-6">
        <button className="bg-green-500 text-white px-4 py-2 rounded" onClick={getPrediction}>Predict Next Expense</button>
        {prediction && <p className="mt-2 text-lg">Predicted next expense: ${prediction}</p>}
      </div>
       {/* Example Chart (dummy data for now) */}
      <LineChart width={400} height={250} data={[{name:1, amt:20},{name:2, amt:40}]}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="name"/>
        <YAxis/>
        <Tooltip/>
        <Line type="monotone" dataKey="amt" stroke="#8884d8"/>
      </LineChart>
    </div>
  );
}