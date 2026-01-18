import os
import threading
from typing import List, Optional, Any, Dict
from contextlib import contextmanager
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine, Result, Row
from sqlalchemy.pool import QueuePool


class DbExecutor:
    """
    Потокобезопасный исполнитель SQL-запросов с использованием SQLAlchemy.
    Реализует паттерн Singleton для единого пула соединений.
    """
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        """Singleton pattern для обеспечения единого пула соединений."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        # Избегаем повторной инициализации
        if hasattr(self, '_initialized'):
            return

        # Используем переменную окружения или значение по умолчанию
        db_url = os.getenv(
            "DATABASE_URL",
            "postgresql+psycopg2://coffee:coffee@localhost:5432/coffeehouse"
        )

        # Настраиваем engine с пулом соединений
        self.engine: Engine = create_engine(
            db_url,
            poolclass=QueuePool,
            pool_size=10,
            max_overflow=20,
            pool_pre_ping=True,  # Проверяем соединения перед использованием
            pool_recycle=3600,  # Переиспользуем соединения каждый час
            echo=False
        )
        self._initialized = True

    @contextmanager
    def get_connection(self):
        """Контекстный менеджер для получения соединения из пула."""
        conn = self.engine.connect()
        try:
            yield conn
        finally:
            conn.close()

    def execute(self, query: str, params: Optional[Dict[str, Any]] = None) -> None:
        """Выполняет запросы без возврата данных (INSERT, UPDATE, DELETE)."""
        try:
            with self.engine.begin() as conn:
                conn.execute(text(query), params or {})
        except Exception as e:
            raise RuntimeError(f"Ошибка выполнения запроса: {e}") from e

    def fetchone(self, query: str, params: Optional[Dict[str, Any]] = None) -> Optional[Row]:
        """Выполняет запрос и возвращает одну строку или None."""
        try:
            with self.get_connection() as conn:
                result: Result = conn.execute(text(query), params or {})
                return result.fetchone()
        except Exception as e:
            raise RuntimeError(f"Ошибка выполнения запроса: {e}") from e

    def fetchall(self, query: str, params: Optional[Dict[str, Any]] = None) -> List[Row]:
        """Выполняет запрос и возвращает все найденные строки."""
        try:
            with self.get_connection() as conn:
                result: Result = conn.execute(text(query), params or {})
                return result.fetchall()
        except Exception as e:
            raise RuntimeError(f"Ошибка выполнения запроса: {e}") from e


