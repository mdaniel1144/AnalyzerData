from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from graph import  MakeGraphNumric,  MakeGraphCategory
import pandas as pd



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

  
    
@app.post("/makeGraphCategory")
async def makeGraphCategory(payload: dict):
    try:

        if 'dfCategory' not in payload:
            raise HTTPException(status_code=400, detail="Your data or intersting col is missing")

        dfCategory = pd.read_json(payload['dfCategory'])
        dfCategoryColumns = dfCategory.columns
                
        print(f"-------------\nMake Graph Numric")  
        graphCategory =  MakeGraphCategory(dfCategory , dfCategoryColumns)
        print("---------------------")
        
        return JSONResponse(status_code=200, content={"graphCategory": graphCategory})
    
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={'message': f"Failed to build database: {str(e.detail)}"})
    except Exception as e:
        print(f"-->Error in server:\n   {str(e)}")
        return JSONResponse(status_code=500, content={'message': f"{str(e)}"})
    


@app.post("/makeGraphNumric")
async def makeGraphNumric(payload: dict):
    try:

        if 'dfNumric' not in payload or 'interstingCol' not in payload or 'top_Correlation' not in payload:
            raise HTTPException(status_code=400, detail="something is missing")

        dfNumric = pd.read_json(payload['dfNumric'])
        interstingCol = payload['interstingCol']
        top_Correlation = pd.Series(dict(payload['top_Correlation']))
                
        print(f"-------------\nMake Graph Numric")  
        graphNumric =  MakeGraphNumric(dfNumric , interstingCol , top_Correlation )
        print("---------------------")
            
        return JSONResponse(status_code=200, content={"graphNumric": graphNumric})
    
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={'message': f"Failed to build database: {str(e.detail)}"})
    except Exception as e:
        print(f"-->Error in server:\n   {str(e)}")
        return JSONResponse(status_code=500, content={'message': f"{str(e)}"})