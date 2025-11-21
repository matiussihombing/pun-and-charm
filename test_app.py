import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_hello(client):
    """Test the root endpoint."""
    rv = client.get('/')
    json_data = rv.get_json()
    assert rv.status_code == 200
    assert json_data == {"message": "Hello from Backend Agent"}

def test_add_numbers(client):
    """Test the add endpoint with valid input."""
    rv = client.post('/add', json={'a': 10, 'b': 20})
    json_data = rv.get_json()
    assert rv.status_code == 200
    assert json_data == {"result": 30}

def test_add_numbers_invalid(client):
    """Test the add endpoint with missing input."""
    rv = client.post('/add', json={'a': 10})
    assert rv.status_code == 400
