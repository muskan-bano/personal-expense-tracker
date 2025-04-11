
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import pandas as pd
from utils import get_db_path, get_transactions, get_budget
import sqlite3

EMAIL_ADDRESS = "your_email@gmail.com"
EMAIL_PASSWORD = "your_app_password"

def send_budget_email(user_email, username, user_id):
    try:
        df = get_transactions(user_id)
        budget = get_budget(user_id)
        if df.empty:
            body = f"Hi {username},\n\nYou have no transactions this month.\n\nBest,\nExpense Tracker"
        else:
            this_month = datetime.now().strftime('%Y-%m')
            df['month'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m')
            this_month_data = df[df['month'] == this_month]
            total_expense = this_month_data[this_month_data['type'] == 'expense']['amount'].sum()
            total_income = this_month_data[this_month_data['type'] == 'income']['amount'].sum()
            body = f"""
Hi {username},

Here's your monthly expense summary:

Total Income: Rs{total_income:.2f}
Total Expenses: Rs{total_expense:.2f}
Budget Limit: Rs{budget:.2f if budget else 0}

"""
            if budget and total_expense > budget:
                body += f"⚠️ You've exceeded your budget by Rs{total_expense - budget:.2f}\n"
            elif budget:
                body += f"✅ You're within budget. Remaining: Rs{budget - total_expense:.2f}\n"
            body += "\nBest,\nExpense Tracker"
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = user_email
        msg['Subject'] = "📊 Your Monthly Expense Summary"
        msg.attach(MIMEText(body, 'plain'))
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
        return True, "Email sent successfully."
    except Exception as e:
        return False, str(e)

def get_budget_recommendation(user_id):
    conn = sqlite3.connect(get_db_path())
    df = pd.read_sql_query("SELECT * FROM transactions WHERE user_id = ?", conn, params=(user_id,))
    conn.close()
    if df.empty:
        return "Not enough data to recommend a budget."
    df['date'] = pd.to_datetime(df['date'])
    df['month'] = df['date'].dt.to_period('M')
    df_expense = df[df['type'] == 'expense']
    monthly_avg = df_expense.groupby('month')['amount'].sum().mean()
    return f"Based on past data, your recommended budget is Rs{monthly_avg:.2f}"
