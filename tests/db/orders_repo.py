from typing import Optional, Dict, Any, List
from tests.db.base_repo import BaseRepository
import allure



class OrderRepository(BaseRepository):
    """Репозиторий для работы с заказами кофе."""

    @allure.step("БД: Получение заказа по ID: {order_id}")
    def get_by_id(self, order_id: int) -> Optional[Dict[str, Any]]:
        """Получает заказ по ID."""
        row = self._db.fetchone("SELECT * FROM coffee_orders WHERE id = :id", {"id": order_id})
        return self._row_to_dict(row)

    @allure.step("БД: Получение всех заказов пользователя ID: {user_id}")
    def get_all_by_user(self, user_id: int) -> List[Dict[str, Any]]:
        """Получает все заказы конкретного пользователя."""
        rows = self._db.fetchall("SELECT * FROM coffee_orders WHERE user_id = :user_id", {"user_id": user_id})
        return self._rows_to_dicts(rows)

    @allure.step("БД: Обновление статуса заказа ID: {order_id} на '{status}'")
    def update_status(self, order_id: int, status: str) -> None:
        """Обновляет статус заказа."""
        self._db.execute(
            "UPDATE coffee_orders SET status = :status WHERE id = :id",
            {"status": status, "id": order_id}
        )

