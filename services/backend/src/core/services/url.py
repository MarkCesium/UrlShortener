from advanced_alchemy import service, repository
from src.core.models.url import URL


class URLService(service.SQLAlchemyAsyncRepositoryService[URL]):
    class Repo(repository.SQLAlchemyAsyncRepository[URL]):
        model_type = URL

    repository_type = Repo
