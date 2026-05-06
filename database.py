import sqlite3
from datetime import datetime

import pandas as pd


DB_NAME = "finguard_ai.db"


def get_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS prediction_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        prediction_type TEXT,
        customer_id TEXT,
        input_summary TEXT,
        risk_score REAL,
        risk_level TEXT,
        decision TEXT,
        source TEXT,
        created_at TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS executive_actions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id TEXT,
        customer_name TEXT,
        branch TEXT,
        segment TEXT,
        risk_type TEXT,
        priority REAL,
        priority_level TEXT,
        recommended_action TEXT,
        status TEXT DEFAULT 'Open',
        created_at TEXT,
        resolved_at TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS audit_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_type TEXT,
        event_message TEXT,
        created_at TEXT
    )
    """)

    conn.commit()
    conn.close()


def save_prediction_log(
    prediction_type,
    customer_id,
    input_summary,
    risk_score,
    risk_level,
    decision,
    source
):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO prediction_logs (
        prediction_type,
        customer_id,
        input_summary,
        risk_score,
        risk_level,
        decision,
        source,
        created_at
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        prediction_type,
        customer_id,
        input_summary,
        risk_score,
        risk_level,
        decision,
        source,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()


def load_prediction_logs(limit=100):
    conn = get_connection()

    df = pd.read_sql_query(
        f"""
        SELECT *
        FROM prediction_logs
        ORDER BY id DESC
        LIMIT {int(limit)}
        """,
        conn
    )

    conn.close()
    return df


def save_executive_action(action):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO executive_actions (
        customer_id,
        customer_name,
        branch,
        segment,
        risk_type,
        priority,
        priority_level,
        recommended_action,
        status,
        created_at,
        resolved_at
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        action.get("customer_id", "UNKNOWN"),
        action.get("customer_name", "Unknown Customer"),
        action.get("branch", "Unknown Branch"),
        action.get("segment", "Retail"),
        action.get("risk_type", "Unknown Risk"),
        float(action.get("priority", 0)),
        action.get("priority_level", "Medium"),
        action.get("recommended_action", "Review case"),
        action.get("status", "Open"),
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        action.get("resolved_at", None)
    ))

    conn.commit()
    conn.close()


def load_executive_actions(limit=200):
    conn = get_connection()

    df = pd.read_sql_query(
        f"""
        SELECT *
        FROM executive_actions
        ORDER BY priority DESC, id DESC
        LIMIT {int(limit)}
        """,
        conn
    )

    conn.close()
    return df


def update_action_status(action_id, status):
    conn = get_connection()
    cur = conn.cursor()

    resolved_at = None
    if status == "Resolved":
        resolved_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cur.execute("""
    UPDATE executive_actions
    SET status = ?, resolved_at = ?
    WHERE id = ?
    """, (
        status,
        resolved_at,
        int(action_id)
    ))

    conn.commit()
    conn.close()


def save_audit_log(event_type, event_message):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO audit_logs (
        event_type,
        event_message,
        created_at
    )
    VALUES (?, ?, ?)
    """, (
        event_type,
        event_message,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()


def load_audit_logs(limit=100):
    conn = get_connection()

    df = pd.read_sql_query(
        f"""
        SELECT *
        FROM audit_logs
        ORDER BY id DESC
        LIMIT {int(limit)}
        """,
        conn
    )

    conn.close()
    return df
