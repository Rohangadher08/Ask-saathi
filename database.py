import sqlite3
import hashlib
import os

DB_FILE = "vyapar_saathi.db"


def get_connection():
    return sqlite3.connect(DB_FILE)


def init_db():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            business_name TEXT NOT NULL,
            business_type TEXT,
            location TEXT,
            monthly_revenue REAL DEFAULT 0,
            monthly_expenses REAL DEFAULT 0,
            existing_emi REAL DEFAULT 0,
            savings REAL DEFAULT 0,
            business_age_years REAL DEFAULT 0,
            expansion_goal TEXT,
            employees INTEGER DEFAULT 0,
            monthly_rent REAL DEFAULT 0,
            monthly_inventory_cost REAL DEFAULT 0,
            owner_experience_years REAL DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()


def hash_password(password):

    return hashlib.sha256(
        password.encode("utf-8")
    ).hexdigest()


def create_user(name, email, password):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute(
            """
            INSERT INTO users
            (name, email, password)
            VALUES (?, ?, ?)
            """,
            (
                name,
                email,
                hash_password(password)
            )
        )

        conn.commit()

        return True, "Account created successfully."

    except sqlite3.IntegrityError:

        return False, "Email already exists."

    finally:

        conn.close()


def login_user(email, password):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, name, email
        FROM users
        WHERE email = ?
        AND password = ?
        """,
        (
            email,
            hash_password(password)
        )
    )

    user = cursor.fetchone()

    conn.close()

    return user


def add_store(user_id, store):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO stores (
            user_id,
            business_name,
            business_type,
            location,
            monthly_revenue,
            monthly_expenses,
            existing_emi,
            savings,
            business_age_years,
            expansion_goal,
            employees,
            monthly_rent,
            monthly_inventory_cost,
            owner_experience_years
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            user_id,
            store["business_name"],
            store["business_type"],
            store["location"],
            store["monthly_revenue"],
            store["monthly_expenses"],
            store["existing_emi"],
            store["savings"],
            store["business_age_years"],
            store["expansion_goal"],
            store["employees"],
            store["monthly_rent"],
            store["monthly_inventory_cost"],
            store["owner_experience_years"]
        )
    )

    conn.commit()
    conn.close()


def get_stores(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM stores
        WHERE user_id = ?
        """,
        (user_id,)
    )

    rows = cursor.fetchall()

    conn.close()

    stores = []

    for row in rows:

        stores.append({
            "id": row[0],
            "user_id": row[1],
            "business_name": row[2],
            "business_type": row[3],
            "location": row[4],
            "monthly_revenue": row[5],
            "monthly_expenses": row[6],
            "existing_emi": row[7],
            "savings": row[8],
            "business_age_years": row[9],
            "expansion_goal": row[10],
            "employees": row[11],
            "monthly_rent": row[12],
            "monthly_inventory_cost": row[13],
            "owner_experience_years": row[14]
        })

    return stores