import pytest
from tests.graphql.core.graphql_client import GraphQLClient
from tests.graphql.service.ingredients_service import IngredientsGQLService
from tests.graphql.service.user_service import UsersGQLService

@pytest.fixture(scope="session")
def gql_client() -> GraphQLClient:
    """Фикстура GraphQL клиента"""
    return GraphQLClient(endpoint_url="http://localhost:8080/graphql")

@pytest.fixture(scope="session")
def ingredients_gql_service(gql_client: GraphQLClient) -> IngredientsGQLService:
    """Фикстура сервиса ингредиентов"""
    return IngredientsGQLService(client=gql_client)

@pytest.fixture(scope="session")
def users_gql_service(gql_client: GraphQLClient) -> UsersGQLService:
    """Фикстура сервиса пользователей"""
    return UsersGQLService(client=gql_client)