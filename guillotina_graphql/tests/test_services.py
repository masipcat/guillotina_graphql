import json
import os
import pytest

DATABASE = os.environ.get("DATABASE", "DUMMY")

pytestmark = pytest.mark.asyncio


@pytest.mark.skipif(DATABASE != "postgres", reason="Only works with pg")
async def test_query(custom_requester):
    async with custom_requester as requester:
        resp, status = await requester(
            "POST",
            "/db/guillotina/",
            data=json.dumps(
                {"id": "my-folder", "@type": "Folder", "title": "My Folder"}
            ),
        )
        assert status == 201, resp

        resp, status = await requester(
            "POST",
            "/db/guillotina/my-folder",
            data=json.dumps({"id": "my-item", "@type": "Item", "title": "My Item"}),
        )
        assert status == 201, resp

        query = """
{
    search(query: {depth: 1}) {
        ... on Folder {
            id
            path
            title
        }
    }
}
        """
        resp, status = await requester(
            "POST",
            "/db/guillotina/@graphql",
            data=json.dumps({"query": query}),
        )
        assert status == 200, resp
        assert resp["data"]["search"] == [
            {
                "id": "my-folder",
                "path": "/my-folder",
                "title": "My Folder",
            }
        ]

        query = """
{
    search(query: {depth: 2}) {
        ... on Item {
            id
            path
            title
            access_users
        }
    }
}
        """
        resp, status = await requester(
            "POST",
            "/db/guillotina/@graphql",
            data=json.dumps({"query": query}),
        )
        assert status == 200, resp
        assert resp["data"]["search"] == [
            {
                "access_users": ["root"],
                "id": "my-item",
                "path": "/my-folder/my-item",
                "title": "My Item",
            }
        ]
