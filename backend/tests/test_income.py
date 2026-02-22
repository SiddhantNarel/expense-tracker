import json


def test_list_income_empty(client):
    resp = client.get('/api/income')
    assert resp.status_code == 200
    data = json.loads(resp.data)
    assert data['data'] == []


def test_create_income(client):
    resp = client.post('/api/income', json={'amount': 10000, 'source': 'Freelance', 'date': '2024-01-01'})
    assert resp.status_code == 201
    data = json.loads(resp.data)
    assert data['amount'] == 10000
    assert data['source'] == 'Freelance'


def test_update_income(client):
    resp = client.post('/api/income', json={'amount': 5000, 'source': 'Family', 'date': '2024-02-01'})
    income_id = json.loads(resp.data)['id']
    resp2 = client.put(f'/api/income/{income_id}', json={'amount': 6000})
    assert resp2.status_code == 200
    assert json.loads(resp2.data)['amount'] == 6000


def test_delete_income(client):
    resp = client.post('/api/income', json={'amount': 3000, 'source': 'Stipend', 'date': '2024-03-01'})
    income_id = json.loads(resp.data)['id']
    resp2 = client.delete(f'/api/income/{income_id}')
    assert resp2.status_code == 200
    resp3 = client.get('/api/income')
    data = json.loads(resp3.data)
    assert all(r['id'] != income_id for r in data['data'])
