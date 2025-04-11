
import sqlite3

def get_db_path():
    return "data.db"

def get_transactions(user_id):
    conn = sqlite3.connect(get_db_path())
    df = pd.read_sql_query("SELECT * FROM transactions WHERE user_id = ?", conn, params=(user_id,))
    conn.close()
    return df

def get_budget(user_id):
    conn = sqlite3.connect(get_db_path())
    cur = conn.cursor()
    cur.execute("SELECT budget_amount FROM budget WHERE user_id = ?", (user_id,))
    result = cur.fetchone()
    conn.close()
    return result[0] if result else 0
