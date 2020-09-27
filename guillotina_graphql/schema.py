from ariadne import make_executable_schema
from ariadne import QueryType
from guillotina.catalog.utils import get_index_fields
from guillotina.component import get_utilities_for
from guillotina.interfaces import IResourceFactory
from guillotina_graphql.mappings import CATALOG_TO_GRAPHQL_MAPPING
from guillotina_graphql.mappings import FIELD_DIRECTIVES_TO_GRAPHQL

query = QueryType()
graphql_schema = None


def build_graphql_schema():
    global graphql_schema

    graphql_schema = make_executable_schema(get_type_defs(), query)


def _iter_model_indices():
    for type_name, schema in get_utilities_for(IResourceFactory):
        for field_name, catalog_info in get_index_fields(type_name).items():
            if field_name in FIELD_DIRECTIVES_TO_GRAPHQL:
                yield type_name, field_name, {
                    "gql_type": FIELD_DIRECTIVES_TO_GRAPHQL[field_name]
                }
            else:
                yield type_name, field_name, catalog_info


def _get_model_fields_and_types():
    # TODO: cache result?
    result_types = {}
    for model, field, directive in _iter_model_indices():
        if model not in result_types:
            result_types[model] = {}

        index_name = directive.get("index_name") or field
        type_ = directive.get("gql_type")
        if not type_:
            type_ = CATALOG_TO_GRAPHQL_MAPPING[directive["type"]]

        result_types[model][index_name] = {"type": type_}
    return result_types


def dict_types_to_graphql_str(dict):
    return "\n    ".join(f"{field}: {value['type']}" for field, value in dict.items())


def _get_input_search_query():
    result_types = _get_model_fields_and_types()
    search_query_fields = {}
    for model in result_types:
        for index_name, directive in result_types[model].items():
            search_query_fields[index_name] = directive

    search_query_raw = "\n    ".join(
        f"{field}: {value['type']}"
        if "default" not in value
        else f"{field}: {value['type']} = {value['default']}"
        for field, value in search_query_fields.items()
    )
    return f"""
        input SearchQuery {{
            _size: Int = 10
            {search_query_raw}
        }}
    """


def _get_models():
    result_types = _get_model_fields_and_types()

    model_types = []
    for model, types in result_types.items():
        model_types += [
            f"type {model} " + "{\n    " + dict_types_to_graphql_str(types) + "}"
        ]
    model_types_str = "\n".join(model_types)

    schema = f"""
{model_types_str}
union SearchResult = {" | ".join(result_types)}
    """
    return schema


def get_type_defs():
    return f"""
        {_get_input_search_query()}

        {_get_models()}

        type Query {{
            search(query: SearchQuery): [SearchResult]
        }}
    """
