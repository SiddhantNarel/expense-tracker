import json


def _add_friend(client, name='Alice'):
    resp = client.post('/api/friends', json={'name': name})
    return json.loads(resp.data)['id']


def test_list_friends_empty(client):
    resp = client.get('/api/friends')
    assert resp.status_code == 200
    assert json.loads(resp.data) == []


def test_create_friend(client):
    resp = client.post('/api/friends', json={'name': 'Bob', 'phone': '9999999999'})
    assert resp.status_code == 201
    assert json.loads(resp.data)['name'] == 'Bob'


def test_create_friend_no_name(client):
    resp = client.post('/api/friends', json={})
    assert resp.status_code == 400


def test_add_transaction_gave(client):
    fid = _add_friend(client)
    resp = client.post(f'/api/friends/{fid}/transactions', json={
        'type': 'gave', 'amount': 500, 'date': '2024-01-01', 'description': 'Dinner'
    })
    assert resp.status_code == 201
    data = json.loads(resp.data)
    assert data['balance'] == 500


def test_add_transaction_received(client):
    fid = _add_friend(client)
    client.post(f'/api/friends/{fid}/transactions', json={'type': 'gave', 'amount': 500, 'date': '2024-01-01'})
    resp = client.post(f'/api/friends/{fid}/transactions', json={
        'type': 'received', 'amount': 200, 'date': '2024-01-02'
    })
    assert resp.status_code == 201
    assert json.loads(resp.data)['balance'] == 300


def test_settle(client):
    fid = _add_friend(client)
    client.post(f'/api/friends/{fid}/transactions', json={'type': 'gave', 'amount': 1000, 'date': '2024-01-01'})
    resp = client.post(f'/api/friends/{fid}/settle', json={'date': '2024-01-10'})
    assert resp.status_code == 201
    assert json.loads(resp.data)['balance'] == 0


def test_partial_settle(client):
    fid = _add_friend(client)
    client.post(f'/api/friends/{fid}/transactions', json={'type': 'gave', 'amount': 1000, 'date': '2024-01-01'})
    resp = client.post(f'/api/friends/{fid}/settle', json={'amount': 400, 'date': '2024-01-10'})
    assert resp.status_code == 201
    assert json.loads(resp.data)['balance'] == 600


def test_transactions_list(client):
    fid = _add_friend(client)
    client.post(f'/api/friends/{fid}/transactions', json={'type': 'gave', 'amount': 100, 'date': '2024-01-01'})
    resp = client.get(f'/api/friends/{fid}/transactions')
    assert resp.status_code == 200
    data = json.loads(resp.data)
    assert len(data['transactions']) == 1
    assert data['balance'] == 100


def test_delete_friend(client):
    fid = _add_friend(client)
    resp = client.delete(f'/api/friends/{fid}')
    assert resp.status_code == 200
    resp2 = client.get('/api/friends')
    assert all(f['id'] != fid for f in json.loads(resp2.data))
