FIELD_DIRECTIVES_TO_GRAPHQL = {
    "id": "String",
    "uuid": "ID",
    "type_name": "String",
    "title": "String",
    "modification_date": "String",
    "creation_date": "String",
    "access_roles": "[String!]",
    "access_users": "[String!]",
    "path": "String",
    "parent_uuid": "String",
    "depth": "Int",
    "tid": "Int",
}


CATALOG_TO_GRAPHQL_MAPPING = {
    "keyword": "String",
    "textkeyword": "String",
    "text": "String",
    "path": "String",
    "int": "Int",
    "float": "Float",
    "date": "String",
    "boolean": "Boolean",
}
