def test_export_expenses_csv(client):
    client.post('/api/expenses', json={'amount': 100, 'date': '2024-01-01', 'payment_method': 'Cash', 'description': 'Test'})
    resp = client.get('/api/export/expenses?from=2024-01-01&to=2024-01-31')
    assert resp.status_code == 200
    assert 'text/csv' in resp.content_type
    data = resp.data.decode()
    assert 'Amount' in data
    assert '100' in data


def test_export_income_csv(client):
    client.post('/api/income', json={'amount': 5000, 'source': 'Family', 'date': '2024-01-01'})
    resp = client.get('/api/export/income?from=2024-01-01&to=2024-01-31')
    assert resp.status_code == 200
    assert 'text/csv' in resp.content_type


def test_export_loans_csv(client):
    resp_friend = client.post('/api/friends', json={'name': 'Charlie'})
    import json
    fid = json.loads(resp_friend.data)['id']
    client.post(f'/api/friends/{fid}/transactions', json={'type': 'gave', 'amount': 200, 'date': '2024-01-01'})
    resp = client.get('/api/export/loans')
    assert resp.status_code == 200
    assert 'text/csv' in resp.content_type


def test_export_report(client):
    resp = client.get('/api/export/report?from=2024-01-01&to=2024-01-31')
    assert resp.status_code == 200
    assert 'text/csv' in resp.content_type
    data = resp.data.decode()
    assert 'Total Income' in data
