from typing import List, Dict, Any
from tests.graphql.models.gql_model import User
from tests.graphql.service.base_gql_service import BaseGQLService


class UsersGQLService(BaseGQLService):
    """Сервис для работы с пользователями через GraphQL"""

    def create(self, user_data: Dict[str, Any]) -> User:
        """
        Создает нового пользователя

        Args:
            user_data: Словарь с данными пользователя
                      {"username": str, "email": str, "password": str, "role": str}
        """
        query = self._load_query("create_user.graphql")

        return self.client.execute(
            query=query,
            step_title=f"GQL: Создание пользователя '{user_data['username']}' с ролью '{user_data['role']}'",
            variables=user_data,
            expected_model=User,
            response_key="createUser"
        )

    def get_by_role(self, role: str) -> List[User]:
        """Получает пользователей по роли"""
        query = self._load_query("get_user_by_role.graphql")
        variables = {"role": role}

        return self.client.execute(
            query=query,
            step_title=f"GQL: Получение пользователей с ролью '{role}'",
            variables=variables,
            expected_model=List[User],
            response_key="users"
        )