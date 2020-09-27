# guillotina_graphql

## Dependencies

Python >= 3.7

Guillotina >= 6.0.0


## Installation

> **Warning:** you need to use a postgres database and have enabled `guillotina.contrib.catalog.pg`

0. Install the plugin:

```bash
pip install guillotina_graphql
```

1. Add `guillotina_graphql` to your settings

```yaml
applications:
 - your_app
 - guillotina_graphql
 - guillotina.contrib.catalog.pg
```

and optionally:
```yaml
graphql:
  enable_playground: true
```

2. You're ready!


## Start using GraphQL

This is the route to the GraphQL endpoint: `http://localhost:8080/<your-db>/<your-container>/@graphql` (needs authentification with permission AccessContent).

You can use the playground on a browser http://localhost:8080/@graphql-playground
