import json


def test_summary(client):
    client.post('/api/expenses', json={'amount': 500, 'date': '2024-01-10', 'payment_method': 'Cash'})
    client.post('/api/income', json={'amount': 10000, 'source': 'Freelance', 'date': '2024-01-05'})
    resp = client.get('/api/analytics/summary?from=2024-01-01&to=2024-01-31')
    assert resp.status_code == 200
    data = json.loads(resp.data)
    assert data['total_expense'] == 500
    assert data['total_income'] == 10000
    assert data['net_savings'] == 9500


def test_category_breakdown(client):
    resp = client.get('/api/analytics/category-breakdown?from=2024-01-01&to=2024-01-31')
    assert resp.status_code == 200
    data = json.loads(resp.data)
    assert isinstance(data, list)


def test_trends(client):
    client.post('/api/expenses', json={'amount': 200, 'date': '2024-01-05', 'payment_method': 'Cash'})
    resp = client.get('/api/analytics/trends?from=2024-01-01&to=2024-01-31&group_by=day')
    assert resp.status_code == 200
    data = json.loads(resp.data)
    assert any(r['period'] == '2024-01-05' for r in data)


def test_income_vs_expense(client):
    resp = client.get('/api/analytics/income-vs-expense?from=2024-01-01&to=2024-03-31')
    assert resp.status_code == 200
    data = json.loads(resp.data)
    assert 'expenses' in data
    assert 'income' in data
