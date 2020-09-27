from ariadne.constants import PLAYGROUND_HTML
from ariadne.graphql import graphql
from guillotina import app_settings
from guillotina import configure
from guillotina.api.service import Service
from guillotina.component import get_utility
from guillotina.interfaces import ICatalogUtility
from guillotina.interfaces import IContainer
from guillotina.response import HTTPNotFound
from guillotina.response import Response
from guillotina.utils import get_current_container
from guillotina_graphql.schema import query


@query.field("search")
async def resolve_search(_, info, *, query):
    container = get_current_container()
    utility = get_utility(ICatalogUtility)
    result = await utility.search(container, query)
    for obj in result["items"]:
        type_name = obj.pop("type_name")
        obj["__typename"] = type_name
    return result["items"]


@configure.service(
    method="GET",
    name="@graphql-playground",
    permission="guillotina.Public",
    allow_access=True,
)
class GraphQlPlaygroundService(Service):
    async def __call__(self):
        if app_settings.get("graphql", {}).get("enable_playground") is True:
            return Response(
                content=PLAYGROUND_HTML,
                headers={"content-type": "text/html"},
            )
        raise HTTPNotFound()


@configure.service(
    method="POST",
    name="@graphql",
    permission="guillotina.AccessContent",
    context=IContainer,
)
class GraphQlService(Service):
    async def __call__(self):
        from guillotina_graphql.schema import graphql_schema

        data = await self.request.json()
        success, response = await graphql(
            graphql_schema,
            data,
            context_value={"request": self.request},
            debug=False,
        )
        status_code = 200 if success else 400
        return Response(
            content=response,
            status=status_code,
            headers={"content-type": "application/json"},
        )
