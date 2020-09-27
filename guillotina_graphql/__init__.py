from guillotina import configure
from guillotina.interfaces import IApplicationConfiguredEvent
from guillotina_graphql.schema import build_graphql_schema

app_settings = {"graphql": {"enable_playground": False}}


def includeme(root):
    """
    custom application initialization here
    """
    configure.scan("guillotina_graphql.services")


@configure.subscriber(for_=(IApplicationConfiguredEvent))
def app_configured(event):
    build_graphql_schema()
