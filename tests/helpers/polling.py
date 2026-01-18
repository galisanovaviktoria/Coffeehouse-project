import time
import logging
from typing import Callable, Any, Optional

logger = logging.getLogger(__name__)


def poll_for_condition(
        predicate: Callable[[], Any],
        timeout: int = 15,
        poll_interval: float = 1.0,
        description: str = "ожидаемого условия"
) -> Optional[Any]:
    """
    Опрашивает условие до тех пор, пока оно не станет истинным.

    Args:
        predicate: Функция, которая возвращает результат или None/False
        timeout: Максимальное время ожидания в секундах
        poll_interval: Интервал между проверками в секундах
        description: Описание того, что мы ждем (для логов)

    Returns:
        Результат predicate или None, если таймаут
    """
    logger.info(f"Начинаем опрос: ожидаем '{description}' в течение {timeout} сек.")
    start_time = time.time()

    while time.time() - start_time < timeout:
        result = predicate()
        if result:  # Если результат не None и не False
            logger.info(f"Успех! Условие '{description}' выполнено.")
            return result
        time.sleep(poll_interval)

    logger.error(f"Таймаут! Не удалось дождаться '{description}' за {timeout} секунд.")
    return None