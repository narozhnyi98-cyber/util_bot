import json
import logging
import sqlite3
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

DATA_DIR = Path(__file__).parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)
DB_FILE = DATA_DIR / "user_data.db"


def init_db():
    """Создаёт таблицу расчётов, если её нет."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS calculations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            calc_type TEXT NOT NULL,
            summary TEXT NOT NULL,
            details TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_user_id ON calculations(user_id)
    """)
    conn.commit()
    conn.close()
    logger.info("База данных инициализирована")


def save_calculation(user_id: int, calc_type: str, summary: str, details: dict):
    """
    Сохраняет расчёт.
    calc_type: 'util' | 'selection' | 'import_check'
    """
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO calculations (user_id, calc_type, summary, details, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (
            user_id,
            calc_type,
            summary,
            json.dumps(details, ensure_ascii=False, default=str),
            datetime.now().isoformat()
        ))
        conn.commit()
        conn.close()
    except Exception as e:
        logger.error(f"Ошибка сохранения расчёта: {e}")


def get_user_calculations(user_id: int, limit: int = 10) -> list:
    """Возвращает последние расчёты пользователя."""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, calc_type, summary, details, created_at
            FROM calculations
            WHERE user_id = ?
            ORDER BY created_at DESC
            LIMIT ?
        """, (user_id, limit))
        rows = cursor.fetchall()
        conn.close()

        result = []
        for row in rows:
            result.append({
                "id": row[0],
                "calc_type": row[1],
                "summary": row[2],
                "details": json.loads(row[3]),
                "created_at": row[4]
            })
        return result
    except Exception as e:
        logger.error(f"Ошибка чтения расчётов: {e}")
        return []


def delete_user_calculations(user_id: int):
    """Удаляет всю историю пользователя."""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM calculations WHERE user_id = ?", (user_id,))
        conn.commit()
        conn.close()
    except Exception as e:
        logger.error(f"Ошибка удаления расчётов: {e}")
