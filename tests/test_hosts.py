import pytest


@pytest.mark.asyncio
async def test_create_host(client):
    r = await client.post("/api/hosts", json={"hostname": "8.8.8.8"})
    assert r.status_code == 201
    assert r.json()["hostname"] == "8.8.8.8"


@pytest.mark.asyncio
async def test_list_hosts(client):
    await client.post("/api/hosts", json={"hostname": "1.1.1.1"})
    r = await client.get("/api/hosts")
    assert r.status_code == 200
    assert len(r.json()) >= 1


@pytest.mark.asyncio
async def test_get_host(client):
    created = await client.post("/api/hosts", json={"hostname": "github.com"})
    r = await client.get(f"/api/hosts/{created.json()['id']}")
    assert r.status_code == 200


@pytest.mark.asyncio
async def test_get_host_not_found(client):
    r = await client.get("/api/hosts/99999")
    assert r.status_code == 404


@pytest.mark.asyncio
async def test_delete_host(client):
    created = await client.post("/api/hosts", json={"hostname": "delete.me"})
    hid = created.json()["id"]
    assert (await client.delete(f"/api/hosts/{hid}")).status_code == 204
    assert (await client.get(f"/api/hosts/{hid}")).status_code == 404