import allure
import json
import logging
from gql import Client
from gql.transport.requests import RequestsHTTPTransport
from typing import Type, TypeVar, Dict, Any, Union
from pydantic import TypeAdapter, ValidationError
from allure_commons.types import AttachmentType

logger = logging.getLogger(__name__)
T = TypeVar("T")


class GraphQLClient:
    """
    Профессиональный GraphQL клиент с полной интеграцией:
    - Логирование всех запросов и ответов
    - Интеграция с Allure для отчетов
    - Автоматический парсинг в Pydantic модели
    - Обработка ошибок
    """

    def __init__(self, endpoint_url: str):
        # Настраиваем транспорт с retry логикой
        transport = RequestsHTTPTransport(
            url=endpoint_url,
            verify=True,
            retries=3,
            timeout=30
        )

        # Создаем клиент с автоматической загрузкой схемы
        self.client = Client(
            transport=transport,
            fetch_schema_from_transport=True
        )

        logger.info(f"GraphQL клиент инициализирован для {endpoint_url}")

    def execute(
            self,
            query,  # queries.queries object (скомпилированный запрос)
            step_title: str,
            variables: Dict[str, Any] = None,
            expected_model: Type[T] = None,
            response_key: str = None
    ) -> Union[T, Dict[str, Any]]:
        """
        Выполняет GraphQL запрос с полным логированием и интеграцией Allure.

        Args:
            query: Скомпилированный GraphQL запрос (queries объект)
            step_title: Заголовок шага для Allure отчета
            variables: Переменные для запроса
            expected_model: Pydantic модель для автоматического парсинга
            response_key: Ключ в ответе GraphQL для извлечения данных

        Returns:
            Типизированный объект (если указана модель) или сырой ответ
        """

        with allure.step(step_title):
            # Логируем начало запроса
            logger.info(f"--> GraphQL Query: {step_title}")

            # Аттачим запрос в Allure
            query_str = str(query).strip()
            allure.attach(
                query_str,
                name="🔍 GraphQL Query",
                attachment_type=AttachmentType.TEXT
            )

            # Логируем и аттачим переменные
            if variables:
                variables_json = json.dumps(variables, indent=2, ensure_ascii=False)
                logger.info(f"    Variables: {variables_json}")
                allure.attach(
                    variables_json,
                    name="📝 Query Variables",
                    attachment_type=AttachmentType.JSON
                )

            try:
                # Выполняем запрос
                result = self.client.execute(query, variable_values=variables or {})

                # Логируем и аттачим ответ
                result_json = json.dumps(result, indent=2, ensure_ascii=False, default=str)
                logger.info(f"<-- GraphQL Response: {result_json}")
                allure.attach(
                    result_json,
                    name="📥 GraphQL Response",
                    attachment_type=AttachmentType.JSON
                )

                # Если модель не указана, возвращаем сырой ответ
                if not expected_model:
                    return result

                # Извлекаем данные по ключу
                if not response_key or response_key not in result:
                    raise KeyError(f"Ключ '{response_key}' не найден в ответе GraphQL")

                data_to_parse = result[response_key]

                # Парсим в Pydantic модель
                try:
                    adapter = TypeAdapter(expected_model)
                    parsed_result = adapter.validate_python(data_to_parse)
                    return parsed_result

                except ValidationError as e:
                    allure.attach(
                        str(e),
                        name="❌ Pydantic Validation Error",
                        attachment_type=AttachmentType.TEXT
                    )
                    raise

            except Exception as e:
                logger.error(f"❌ Ошибка выполнения GraphQL запроса: {e}")
                allure.attach(
                    str(e),
                    name="❌ GraphQL Execution Error",
                    attachment_type=AttachmentType.TEXT
                )
                raise