import os
from gql import gql
from tests.graphql.core.graphql_client import GraphQLClient


class BaseGQLService:
    """
    Базовый класс для всех GraphQL сервисов.

    Предоставляет:
    - Загрузку запросов из файлов
    - Доступ к GraphQL клиенту
    - Общую функциональность для наследников
    """

    def __init__(self, client: GraphQLClient):
        # Определяем путь к папке с запросами
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.queries_path = os.path.abspath(os.path.join(current_dir, '..', 'queries'))

        self.client = client

    def _load_query(self, file_name: str):
        """
        Загружает и компилирует GraphQL запрос из файла.

        Args:
            file_name: Имя файла с расширением .graphql

        Returns:
            Скомпилированный gql объект
        """
        file_path = os.path.join(self.queries_path, file_name)

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                query_string = f.read()
                return gql(query_string)

        except FileNotFoundError:
            raise FileNotFoundError(
                f"GraphQL запрос не найден: {file_path}\n"
                f"Убедитесь, что файл существует и путь корректен."
            )
        except Exception as e:
            raise RuntimeError(f"Ошибка загрузки GraphQL запроса {file_name}: {e}")