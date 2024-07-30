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

table_fixkey = {
    "name": "plants",
    "size": [5, 3],
    "primaryKey": "id_plants",
    "foreignKey": "",
    "reference": "",
    "columns": [{"name": "id_plants", "valueType": "category"}, {"name": "name", "valueType": "category"} , {"name": "mass", "valueType": "float64"}],
    "rows": [["1", "earth" , 1.0],["2", "earth" , 1.0] , ["", "earth" , 1.0], ["2", "sun" ,  2.4] , ["3",  "moon" , 3.6]],
    "is_readable": True,
}

table_data_1 = {
    "name": "people",
    "size": [3, 3],
    "primaryKey": "id_people",
    "foreignKey": "id_plants",
    "reference": "plants",
    "columns": [{"name": "id_people", "valueType": "category"}, {"name": "id_plants", "valueType": "category"}, {"name": "name", "valueType": "category"} , {"name": "age", "valueType": "float64"}],
    "rows": [["1", "1" , "Daniel", 35], ["2", "1" , "Yossi", 11] , ["3",  "3" , "Rotem", 15] , ["4",  "3" , "Rom", 25]],
    "is_readable": True,
}

listData = [table_data , table_data_1]
name  = "test_table"
primaryKey = "id_plants"



def test_create_upload_file_csv():
    file_path = "../files/train.csv"  # Provide a valid path to a test CSV file
    with open(file_path, "rb") as file:
        files = {"file": (file.name, file, "application/json")}
        data = {"primaryKey": "User_ID", "foreignKey": "", "reference": ""}
        response = client.post("/uploadfile/", files=files, data=data)
        
    response_json = response.json()
    assert response.status_code == 200 
    assert "table" in response_json
    assert response_json["table"]["primaryKey"] == "User_ID"
    assert response_json["table"]["size"][1] == 10
    assert response_json["table"]["size"][0] == 2000

def test_create_upload_file_json():
    file_path = "../files/test.json"  # Provide a valid path to a test CSV file
    with open(file_path, "rb") as file:
        files = {"file": (file.name, file, "application/json")}
        response = client.post("/uploadfile/", files=files, data={"primaryKey": "A","foreignKey": "", "reference": ""})
        
    response_json = response.json()
    assert response.status_code == 200 
    assert "table" in response_json
    assert response_json["table"]["primaryKey"] == "A"
    assert response_json["table"]["size"][1] == 3
    assert response_json["table"]["size"][0] == 3
    
   

def test_create_upload_json():
    payload = {
        "json": json_data,
        "name": name,
        "primaryKey": primaryKey,
        "foreignKey": "",
        "reference": ""
    }
    
    response = client.post("/uploadJson/", json=payload)
    assert response.status_code == 200
    response_json = response.json()
    print(response_json)
    assert "table" in response_json
    assert response_json["table"]["name"] == name
    assert response_json["table"]["rows"][0][2] == 1.0
    assert response_json["table"]["size"][1] == 3



def test_checkSetting():
    payload = {
        "data": table_data,
        "name": name,
        "primaryKey" : "name",
        "foreignKey": "",
        "reference": "",
        "newCols" : [{"name": "id_plants", "valueType": "category"}, {"name": "name", "valueType": "category"}],
    }
    response = client.post("/checkSetting" ,json=payload )
    response_json = response.json()
    print(response_json)
    assert response.status_code == 200
    assert "table" in response_json
    assert response_json["table"]
    assert response_json["table"]["size"][1] == 2
    assert response_json["table"]["columns"][0]["name"] == "id_plants"
    assert response_json["table"]["primaryKey"] == "name"
    
    
def test_fixKey():
    payload = {
        "data": table_fixkey,
        "primaryKey" : "name",
        "foreignKey": "",
    }
    response = client.post("/fixKeys" ,json=payload )
    response_json = response.json()
    print(response_json)
    assert response.status_code == 200
    assert "table" in response_json
    assert response_json["message"]['type'] == 'succses'
    

def test_summary(mocker):
    payload = {
        "table": table_data,
        "interstingCol": "name"
    }
    
    mocker.patch("httpx.AsyncClient.post", return_value=MockResponse(status_code=200, json_data={"graphCategory": ["010110001","010110001"], "graphNumric": []}))

    response = client.post("/summary" ,json=payload )
    response_json = response.json()
    assert response.status_code == 200
    assert "summary" in response_json
    assert response_json["summary"]
    assert response_json["summary"]["name"] == "plants"
    assert response_json["summary"]["count"] == "plants 3 Objects"
    assert len(response_json["summary"]["graphCategory"]) == 2
    assert response_json["summary"]["graphNumric"] != None
 
 
def test_sqlQuery(mocker):
    payload = {
        "listData": listData,
        "query": "select name from plants where id_plants == 1"
    }
    
    mocker.patch("httpx.AsyncClient.post", return_value=MockResponse(status_code=200, json_data={"results": [{'name':"earth"}]}))

    response = client.post("/makeQuery" ,json=payload )
    response_json = response.json()
    assert response.status_code == 200
    assert "results" in response_json
    assert response_json["results"]
    assert response_json["results"][0]['name'] == "earth"
    

def test_buildDatabase(mocker):
    payload = {
        "listData": listData,
    }
    
    mocker.patch("httpx.AsyncClient.post", return_value=MockResponse(status_code=200, json_data={'media_type':'application/sql' ,'headers':{'content-type' : 'application/sql','Content-Disposition': 'attachment; filename=database.sql'}}))

    response = client.post("/BuildDatabase" ,json=payload )

    assert response.status_code == 200

    
class MockResponse:
    def __init__(self, status_code, json_data , content=None):
        self.status_code = status_code
        self._json = json_data
        self.content = content or b""

    
    def json(self):
        return self._json