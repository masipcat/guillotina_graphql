from guillotina import testing
from guillotina.tests.fixtures import ContainerRequesterAsyncContextManager
from pytest_docker_fixtures import images

import json
import pytest

images.configure("postgresql", "postgres", "11.6")


def base_settings_configurator(settings):
    settings["load_utilities"]["catalog"] = {
        "factory": "guillotina.contrib.catalog.pg.PGSearchUtility",
        "provides": "guillotina.interfaces.ICatalogUtility",
    }

    if "applications" in settings:
        settings["applications"].append("guillotina_graphql")
    else:
        settings["applications"] = ["guillotina_graphql"]
    settings["applications"] += ["guillotina.contrib.catalog.pg"]


testing.configure_with(base_settings_configurator)


class guillotina_graphql_Requester(ContainerRequesterAsyncContextManager):  # noqa
    async def __aenter__(self):
        await super().__aenter__()
        await self.requester(
            "POST",
            "/db/guillotina/@addons",
            data=json.dumps({"id": "guillotina_graphql"}),
        )
        return self.requester


@pytest.fixture(scope="function")
async def custom_requester(guillotina):
    return guillotina_graphql_Requester(guillotina)
