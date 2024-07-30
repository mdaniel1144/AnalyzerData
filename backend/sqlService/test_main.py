from fastapi.testclient import TestClient
from main import app  # Import your FastAPI app


client = TestClient(app)

json_data = """{
    "id_plants": [1, 2, 3],
    "name": ["earth", "sun", "moon"],
    "mass": [1.0, 2.4, 3.6]
}"""

table_data = {
    "name": "plants",
    "size": [3, 3],
    "primaryKey": "id_plants",
    "foreignKey": "",
    "reference": "",
    "columns": [{"name": "id_plants", "valueType": "category"}, {"name": "name", "valueType": "category"} , {"name": "mass", "valueType": "float64"}],
    "rows": [["1", "earth" , 1.0], ["2", "sun" ,  2.4] , ["3",  "moon" , 3.6]],
    "is_readable": True,
}

table_data_1 = {
    "name": "people",
    "size": [4, 4],
    "primaryKey": "id_people",
    "foreignKey": "id_plants",
    "reference": "plants",
    "columns": [{"name": "id_people", "valueType": "category"}, {"name": "id_plants", "valueType": "category"}, {"name": "name", "valueType": "category"} , {"name": "age", "valueType": "float64"}],
    "rows": [["1", "1" , "Daniel", 35], ["2", "1" , "Yossi", 11] , ["3",  "3" , "Rotem", 15] , ["4",  "3" , "Rom", 25]],
    "is_readable": True,
}

listData = [table_data , table_data_1]
  

def test_checkSqlQuery():
    payload = {
        "listData": listData,
        "query": """SELECT people.id_people, people.name AS person_name, people.age, 
                    plants.name AS plant_name, plants.mass
                    FROM people
                    JOIN plants ON people.id_plants = plants.id_plants;"""
    }
    response = client.post("/makeQuery" ,json=payload )
    response_json = response.json()

    assert response.status_code == 200
    if  response.status_code == 200:
        assert response_json["results"] != None
        assert response_json["results"][1]["age"] == 11
        assert response_json["results"][1]["person_name"] == "Yossi"

    
def test_checkBuildingDatabase():
    payload = {
        "listData": listData,
    }
    
    response = client.post("/BuildDatabase" ,json=payload )
    
    assert response.status_code == 200
    if  response.status_code == 200:
        assert response.content[:5] == b"BEGIN"