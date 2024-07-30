from fastapi import FastAPI, HTTPException , UploadFile , File , Form
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from schemas import Table , Column , Summary
from config import MAX_UNIQUE , MAX_GRAPH_NUMRIC
import pandas as pd
import io 
import json
import httpx



app = FastAPI()
origins = [
    "http://localhost:3000",  # React frontend URL
    "https://yourproductiondomain.com",  # Production frontend URL (if applicable)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],  # Methods allowed by CORS
    allow_headers=["Authorization", "Content-Type"],  # Headers allowed by CORS
)


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...), primaryKey: str = Form(...), foreignKey: str = Form(None), reference: str = Form(None)):
    try:
        content_type = ""
        name = ""

        if file is None or primaryKey is None:
            raise HTTPException(status_code=422, detail="File or primary_Key is missing")
    
        # Read the uploaded file into a pandas DataFrame
        print("------------------\nMake table from csv file")
        print(f"primaryKey: {primaryKey}\nfile: {file.filename}\nforeignKey:{foreignKey}\nreference:{reference}")
        
        content = await file.read()
        
        if file.filename.endswith('.csv'):
            content_type = 'text/csv'
            name = file.filename.replace(".csv", "")
        elif file.filename.endswith('.json'):
            content_type = 'application/json'
            name = file.filename.replace(".json", "")
        else:
            raise HTTPException(status_code=415, detail="Unsupported file type.\nOnly CSV or JSON files are allowed.")
        
        
        if content_type == "text/csv":
            for encoding in ['utf-8', 'latin1', 'iso-8859-1', 'utf-16']:
                try:
                    df = pd.read_csv(io.BytesIO(content), encoding=encoding)
                    break  # Break the loop if successful
                except UnicodeDecodeError:
                    continue #---> to the next encode
            else:
                raise UnicodeDecodeError("Unable to decode file with any encoding")
        else:
            try:
                data = json.loads(content.decode())
                df = pd.json_normalize(data)
            except json.JSONDecodeError:
                raise HTTPException(status_code=400, detail="Invalid JSON format")
            except Exception as e:
                raise "Error - at tring open json file"

        table = BuildTable(df ,name = name ,primaryKey= primaryKey , foreignKey=foreignKey , reference=reference)
        print("-------------------")
        return {"message": {"type": "succses" ,"content" : "succseful make dataframe"},"table": table}
    
    except HTTPException as e:
        return {"message": {"type": "error" ,"content" : f"Error {str(e)}"} , "table": None}
    except UnicodeDecodeError as e:
        return {"message": {"type": "error" ,"content" : f"Error - This doc is unreadable: {e}"} , "table": None}
    except KeyError as e:
        return {"message": {"type": "error" ,"content" : f"Error - Your Error Key {str(e)} not found"} , "table": None}
    except Exception as e:
        print(f"Error In Server: {e}\n-------------------")
        return {"message": {"type": "error" ,"content" : f"Error {str(e)}"} , "table": None}


@app.post("/uploadJson/")
async def create_upload_file(item: dict):
    try:
        if 'json' not in item or 'name' not in item or 'primaryKey'  not in item:
            raise HTTPException(status_code=400, detail="item must contain 'name', 'json',primaryKey keys")

        name = item["name"]
        primaryKey = item["primaryKey"]
        foreignKey = item["foreignKey"]
        reference = item["reference"]
        json = io.StringIO(item["json"])

        # Read the uploaded file into a pandas DataFrame
        df = pd.read_json(json)
        table = BuildTable(df,name = name , primaryKey=primaryKey ,foreignKey=foreignKey , reference=reference)
        print("------------------\nMake table from JSON file\n-------------------")
        
        return {"message": {"type": "succses" ,"content" : "succseful make dataframe"},"table": table}
    except HTTPException as e:
        return {"message": {"type": "error" ,"content" : f"Error {str(e)}"} ,"table": None}
    except KeyError as e:
        return {"message": {"type": "error" ,"content" : f"Error - Your Error Key {str(e)} not found"} ,"table": None}
    except Exception as e:
        return {"message": {"type": "error" ,"content" : f"Error {str(e)}"} ,"table": None}



def BuildTable(df: pd.DataFrame , name: str , primaryKey:str , foreignKey: str ,reference: str ):
    # Extract information

    size = df.shape
    columns = []
    rows = df.values.tolist()   #--> list of list
    
    if not df[primaryKey].is_unique:
        print("Your primary key for this table is not recommend")
        
    if foreignKey in df.columns and foreignKey:
        if not df[foreignKey].is_unique:
            print("Your foreign Key for this table is not recommend")
            
    for col in df.columns:
        column = Column(name = col, valueType= str(df[col].dtype))
        columns.append(column)
        
    table = Table(
        name=name,
        size = size,
        primaryKey= primaryKey,
        foreignKey= "" if foreignKey is None else str(foreignKey),
        reference= reference,
        columns=columns,
        rows= rows,
        is_readable = True,
    )
    
    return table
 
def FixTheDataSet(df: pd.DataFrame, interstingCol: str, primaryKey:str):

    if(df[interstingCol].dtype in ['int64', 'float64']):
        q25 = df[interstingCol].quantile(0.25)
        q75 = df[interstingCol].quantile(0.75)

         # Calculate the IQR
        iqr = q75 - q25
        # Identify values that are more than 1.5 times the IQR below the 25th percentile or above the 75th percentile
        df = df[(df[interstingCol] > q25 - 1.5*iqr) & (df[interstingCol] < q75 + 1.5*iqr)]
    
    #convert all col is object/category and unique to category
    object_columns = df.select_dtypes(include=['object']).columns.difference([primaryKey])
    df.loc[:, object_columns] = df.loc[:, object_columns].apply(lambda x: x.str.lower())
    
    # Drop identified columns from dataframe which there unique is greater than MaX_uNIQUE
    category_cols_to_drop = []
    for col in df.columns:
        if df[col].nunique() <= MAX_UNIQUE and df[col].dtype in ['category', 'object']:
            df = df.assign(**{col: df[col].astype('category')})
        else:
            category_cols_to_drop.append(col)
        

    #df['date_column'] = pd.to_datetime(df['date_column'], errors='coerce')
    df = df.drop_duplicates(subset=[primaryKey], keep="first").copy()
    df = df.dropna(how="any", axis=0).copy()  # Drop rows with at least 2 None/null values
    
    return df
    
    
@app.post("/summary")
async def get_summary(payload: dict):
    try:

        if 'table' not in payload or 'interstingCol' not in payload:
            raise HTTPException(status_code=400, detail="Your data or intersting col is missing")

        table_data = payload['table']
        interstingCol = payload['interstingCol']
        
        table = Table(**table_data)
        
        print(f"-------------\nConnect to Graph Service..")
        print(table.name)
        print(interstingCol)
        
        df = table.to_dataframe()
        dfCopy = FixTheDataSet(df , interstingCol=interstingCol , primaryKey=table.primaryKey).copy()
        print(f"Fixed the dataset")
        
        name = table.name
        count = f"{table.name} {dfCopy.shape[0]} Objects"

        dfCategory = dfCopy.select_dtypes(include=['category'])
        dfCategory[interstingCol] = dfCopy[[interstingCol]]
        dfNumric = dfCopy.select_dtypes(include=['int64', 'float64'])
        print(df.info())
        print(dfCategory.info())
        print(dfNumric.info())
        
        top_Correlation = []
        correlation_matrix = dfNumric.corr()
        if interstingCol in dfNumric.columns:
            correlation = correlation_matrix[interstingCol].abs()
            correlation = correlation.drop(interstingCol)                       #Delete the col which intersting
            top_Correlation = correlation.nlargest(MAX_GRAPH_NUMRIC)            # Get top correlated columns
         
        payloadGraph_1  = {
            'dfNumric' : dfNumric.to_json(),
            'interstingCol' : interstingCol,
            'top_Correlation' : list(top_Correlation.items())
        }

        payloadGraph_2  = {
            'dfCategory' : dfCategory.to_json(),
        }
        
        async with httpx.AsyncClient() as client:
            response_graphNumric = await client.post("http://graphservice:9000/makeGraphNumric", json=payloadGraph_1)
            response_graphCategory = await client.post("http://graphservice:9000/makeGraphCategory", json=payloadGraph_2)   
        
        if response_graphNumric.status_code == 200 and response_graphCategory.status_code == 200:
            summary = Summary(
                name = name,
                interstingCol = interstingCol,
                count = count,
                interstingColDescription = df[[interstingCol]].describe(include="all").to_dict(),       
                graphCategory =  response_graphCategory.json()['graphCategory'],
                graphNumric =  response_graphNumric.json()['graphNumric'],
            )
        elif response_graphNumric.status_code != 200:
            raise HTTPException(status_code=response_graphNumric.status_code, detail=response_graphNumric.json())
        else:
            raise HTTPException(status_code=response_graphCategory.status_code, detail=response_graphCategory.json())

        print("---------------------")
        
        return {"message": {"type": "succses" ,"content": "Succsesfull Make Summary"},"summary": summary}
    
    except HTTPException as e:
        return {"message": {"type": "error" ,"content": f"Error {str(e)}"},"summary": None}
    except KeyError as e:
        return {"message": {"type": "error" ,"content": f"Error {str(e)}"},"summary": None}
    except Exception as e:
        print(f"Error in server: {str(e)}")
        return {"message": {"type": "error" ,"content": f"Error {str(e)}"},"summary": None}
    
@app.post("/checkSetting")
async def CheckTypes(payload: dict):
    try:

        if 'data' not in payload or 'newCols' not in payload or 'primaryKey' not in payload or 'name' not in payload or 'foreignKey' not in payload or 'reference' not in payload:
            raise HTTPException(status_code=400, detail="Something is missing")

        data = payload['data']
        name = payload['name']
        primaryKey = payload['primaryKey']
        foreignKey = payload['foreignKey']
        reference = payload['reference']
        newCols = payload['newCols']
                
        table = Table(**data)
        
        print(f"-------------\nMake Checking for {table.name}")
 
        
        df = table.to_dataframe()
        listName = [item["name"] for item in newCols]
        print(listName)
        for col in df.columns:
            if col in listName:
                print(col)
                element = [item for item in newCols if item.get("name") == col]
                df = df.assign(**{col: df[col].astype(element[0]["valueType"])})
            else:
                df = df.drop(columns=[col])

        table = BuildTable(df=df , name=name , primaryKey=primaryKey , foreignKey=foreignKey , reference = reference)

        print("---------------------")
        return {"message": {"type": "succses" ,"content": "succseful update setting"},"table": table}
    
    except HTTPException as e:
        return {"message": {"type": "error" ,"content": f"Error {str(e)}"},"table": None}
    except KeyError as e:
        return {"message": {"type": "error" ,"content": f"Error {str(e)}"},"table": None}
    except Exception as e:
        print(f"Error in server: {str(e)}")
        return {"message": {"type": "error" ,"content": f"Error {str(e)}"},"table": None}

@app.post("/fixKeys")
async def fixKeys(payload: dict):
    try:

        if 'data' not in payload or 'primaryKey' not in payload or 'foreignKey' not in payload:
            raise HTTPException(status_code=400, detail="Something is missing")

        data = Table(**payload['data'])
        primaryKey = payload['primaryKey']
        foreignKey = payload['foreignKey']
        
        print("-----------\nMake Fix Keys")
        df = data.to_dataframe()
        df.drop_duplicates(subset=[primaryKey] , inplace=True)
        df.dropna(subset=[primaryKey], inplace=True)
        
        if foreignKey != "":
            df.drop_duplicates(subset=[foreignKey] , inplace=True)

        table = BuildTable(df=df , name=data.name , primaryKey=primaryKey , foreignKey=foreignKey , reference=data.reference)

        print("---------------------")
        return {"message": {"type": "succses" ,"content": "succseful Fix Key"},"table": table}
    
    except HTTPException as e:
        return {"message": {"type": "error" ,"content": f"Error {str(e)}"},"table": None}
    except KeyError as e:
        return {"message": {"type": "error" ,"content": f"Error {str(e)}"},"table": None}
    except Exception as e:
        print(f"Error in server: {str(e)}")
        return {"message": {"type": "error" ,"content": f"Error {str(e)}"},"table": None}
    


@app.post("/makeQuery")
async def MakeQuery(payload: dict):
    try:
   
        print(f"-------------\nConnection SQL Service..")
        async with httpx.AsyncClient() as client:
            response = await client.post("http://sqlservice:8888/makeQuery", json=payload)
        print("---------------------")
        
        if response.status_code == 200:
            return JSONResponse(status_code=200, content=response.json())
        else:
            raise HTTPException(status_code=response.status_code, detail=response.json())
            
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content=e.detail)
    except Exception as e:
        print(f"-->Error in server:\n   {str(e)}")
        return JSONResponse(status_code=500, content={'message': f"{str(e)}"})
    
    
@app.post("/BuildDatabase")
async def BuildDatabase(payload: dict):
    try:
        
        print(f"-------------\nConnection SQL Service..")
        async with httpx.AsyncClient() as client:
            response = await client.post("http://sqlservice:8888/BuildDatabase", json=payload)
        print("---------------------")
        
        if response.status_code == 200:
            return StreamingResponse(io.BytesIO(response.content), media_type='application/sql', headers={'Content-Disposition': 'attachment; filename=database.sql'})
        else:
            raise HTTPException(status_code=response.status_code, detail=response.json())
    
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content=e.detail)
    except Exception as e:
        print(f"-->Error in server:\n   {str(e)}")
        return JSONResponse(status_code=500, content={'message': f"{str(e)}"})

        