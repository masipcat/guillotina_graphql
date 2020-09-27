from guillotina.component import get_utility
from guillotina.interfaces import ICatalogUtility
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
