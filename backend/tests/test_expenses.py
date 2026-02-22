import json


def test_list_expenses_empty(client):
    resp = client.get('/api/expenses')
    assert resp.status_code == 200
    data = json.loads(resp.data)
    assert data['data'] == []
    assert data['total'] == 0


def test_create_expense(client):
    payload = {'amount': 500, 'date': '2024-01-15', 'description': 'Lunch', 'payment_method': 'Cash'}
    resp = client.post('/api/expenses', json=payload)
    assert resp.status_code == 201
    data = json.loads(resp.data)
    assert data['amount'] == 500
    assert data['description'] == 'Lunch'


def test_create_expense_invalid_amount(client):
    resp = client.post('/api/expenses', json={'amount': -10, 'date': '2024-01-15'})
    assert resp.status_code == 400


def test_create_expense_invalid_date(client):
    resp = client.post('/api/expenses', json={'amount': 100, 'date': 'not-a-date'})
    assert resp.status_code == 400


def test_get_expense(client):
    resp = client.post('/api/expenses', json={'amount': 200, 'date': '2024-02-01', 'payment_method': 'GPay'})
    expense_id = json.loads(resp.data)['id']
    resp2 = client.get(f'/api/expenses/{expense_id}')
    assert resp2.status_code == 200
    assert json.loads(resp2.data)['id'] == expense_id


def test_get_expense_not_found(client):
    resp = client.get('/api/expenses/9999')
    assert resp.status_code == 404


def test_update_expense(client):
    resp = client.post('/api/expenses', json={'amount': 300, 'date': '2024-03-01', 'payment_method': 'Cash'})
    expense_id = json.loads(resp.data)['id']
    resp2 = client.put(f'/api/expenses/{expense_id}', json={'amount': 350, 'description': 'Updated'})
    assert resp2.status_code == 200
    data = json.loads(resp2.data)
    assert data['amount'] == 350
    assert data['description'] == 'Updated'


def test_delete_expense(client):
    resp = client.post('/api/expenses', json={'amount': 100, 'date': '2024-01-01', 'payment_method': 'Cash'})
    expense_id = json.loads(resp.data)['id']
    resp2 = client.delete(f'/api/expenses/{expense_id}')
    assert resp2.status_code == 200
    resp3 = client.get(f'/api/expenses/{expense_id}')
    assert resp3.status_code == 404


def test_filter_expenses_by_date(client):
    client.post('/api/expenses', json={'amount': 100, 'date': '2024-01-01', 'payment_method': 'Cash'})
    client.post('/api/expenses', json={'amount': 200, 'date': '2024-02-01', 'payment_method': 'Cash'})
    resp = client.get('/api/expenses?from=2024-01-01&to=2024-01-31')
    data = json.loads(resp.data)
    assert data['total'] == 1
    assert data['data'][0]['amount'] == 100


def test_pagination(client):
    for i in range(5):
        client.post('/api/expenses', json={'amount': i + 1, 'date': '2024-01-01', 'payment_method': 'Cash'})
    resp = client.get('/api/expenses?page=1&per_page=3')
    data = json.loads(resp.data)
    assert len(data['data']) == 3
    assert data['total'] == 5
    assert data['pages'] == 2
