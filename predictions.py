# predictions.py

import streamlit as st
import yfinance as yf
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

def get_stock_data(symbol):
    stock = yf.Ticker(symbol)
    df = stock.history(period="max")
    return df

def prepare_data(df):
    df['Previous_Close'] = df['Close'].shift(1)
    df.dropna(inplace=True)
    return df

def train_model(df):
    X = df[['Previous_Close']]
    y = df['Close']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)

    train_score = model.score(X_train, y_train)
    test_score = model.score(X_test, y_test)
    return model, train_score, test_score

def predict_stock_price(model, user_data):
    previous_close = user_data['Previous_Close']
    predicted_price = model.predict([[previous_close]])
    return predicted_price[0]

def display_predicted_price(predicted_price):
    st.write(f"Predicted next day's stock price: ${predicted_price:.2f}")

def get_user_data(symbol):
    df = get_stock_data(symbol)
    if not df.empty:
        df = prepare_data(df)
        trained_model, _, _ = train_model(df)

        user_data = {'Previous_Close': df.iloc[-1]['Close']}
        return trained_model, user_data
    return None, None

def render_predictions(symbol):
    st.header('Stock Price Prediction')
    trained_model, user_data = get_user_data(symbol)
    if trained_model and user_data:
     predicted_price = predict_stock_price(trained_model, user_data)
     display_predicted_price(predicted_price)
    else:
       st.write("Error predicting stock price. Please try again.")
