import json


def test_set_budget(client):
    resp = client.post('/api/budgets', json={'amount': 15000, 'month': 1, 'year': 2024})
    assert resp.status_code == 201
    data = json.loads(resp.data)
    assert data['amount'] == 15000


def test_list_budgets(client):
    client.post('/api/budgets', json={'amount': 5000, 'month': 2, 'year': 2024})
    resp = client.get('/api/budgets?month=2&year=2024')
    data = json.loads(resp.data)
    assert len(data) == 1
    assert data[0]['amount'] == 5000


def test_delete_budget(client):
    resp = client.post('/api/budgets', json={'amount': 3000, 'month': 3, 'year': 2024})
    budget_id = json.loads(resp.data)['id']
    resp2 = client.delete(f'/api/budgets/{budget_id}')
    assert resp2.status_code == 200
    resp3 = client.get('/api/budgets?month=3&year=2024')
    assert json.loads(resp3.data) == []


def test_upsert_budget(client):
    client.post('/api/budgets', json={'amount': 5000, 'month': 4, 'year': 2024})
    resp = client.post('/api/budgets', json={'amount': 7000, 'month': 4, 'year': 2024})
    assert resp.status_code == 201
    resp2 = client.get('/api/budgets?month=4&year=2024')
    data = json.loads(resp2.data)
    assert len(data) == 1
    assert data[0]['amount'] == 7000
