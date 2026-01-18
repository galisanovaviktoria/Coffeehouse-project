import pytest
import allure
from tests.graphql.service.user_service import UsersGQLService


@pytest.mark.graphql
@pytest.mark.users
@allure.feature("GraphQL API: Пользователи")
class TestUsersGQL:

    @allure.story("Создание пользователя с разными ролями")
    @pytest.mark.parametrize("role", ["CUSTOMER", "SELLER", "ADMIN"])
    def test_create_user_with_role(
            self,
            users_gql_service: UsersGQLService,
            faker_instance,
            role: str
    ):
        """Тест создания пользователей с разными ролями"""

        # Подготавливаем данные
        user_data = {
            "username": f"gql_{role.lower()}_{faker_instance.user_name()}",
            "email": faker_instance.email(),
            "password": faker_instance.password(length=12),
            "role": role
        }

        # Создаем пользователя
        created_user = users_gql_service.create(user_data)

        # Проверяем результат
        assert created_user.username == user_data["username"]
        assert created_user.email == user_data["email"]
        assert created_user.role == role
        assert created_user.id is not None

    @allure.story("Получение пользователей по роли")
    def test_get_users_by_role(self, users_gql_service: UsersGQLService, faker_instance):
        """Тест получения пользователей по роли"""

        # Создаем пользователя с определенной ролью
        user_data = {
            "username": f"gql_customer_{faker_instance.user_name()}",
            "email": faker_instance.email(),
            "password": "password123",
            "role": "CUSTOMER"
        }

        created_user = users_gql_service.create(user_data)

        # Получаем всех пользователей с ролью CUSTOMER
        customers = users_gql_service.get_by_role("CUSTOMER")

        # Проверяем результат
        assert isinstance(customers, list)
        assert len(customers) > 0

        # Проверяем, что наш пользователь в списке
        customer_ids = [user.id for user in customers]
        assert created_user.id in customer_ids

        # Проверяем, что все пользователи имеют правильную роль
        for customer in customers:
            assert customer.role == "CUSTOMER"