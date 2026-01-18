from typing import List
from tests.graphql.models.gql_model import Ingredient
from tests.graphql.service.base_gql_service import BaseGQLService


class IngredientsGQLService(BaseGQLService):
    """Сервис для работы с ингредиентами через GraphQL"""

    def get_all(self) -> List[Ingredient]:
        """Получает все ингредиенты"""
        query = self._load_query("get_all_ingredients.graphql")
        return self.client.execute(
            query=query,
            step_title="GQL: Получение всех ингредиентов",
            expected_model=List[Ingredient],
            response_key="ingredients"
        )