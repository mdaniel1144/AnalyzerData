from fastapi.testclient import TestClient
from main import app  # Import your FastAPI app


client = TestClient(app)


def test_make_graph_numric_success():
    payload = {
        'dfNumric': '{"mass": [10.2, 21.6, 36.2], "year": [2011, 2019, 2024]}',
        'interstingCol': 'mass',
        'top_Correlation': [0.5, 0.6, 0.7]
    }
    
    response = client.post('/makeGraphNumric', json=payload)
    assert response.status_code == 200
    assert 'graphNumric' in response.json()

    
def test_make_graph_numric_success():
    payload = {
        'dfCategory': '{"id_plants": [1, 2, 3], "name": ["earth", "moon", "sun"]}',
    }
    
    response = client.post('/makeGraphCategory', json=payload)
    assert response.status_code == 200
    assert 'graphCategory' in response.json()