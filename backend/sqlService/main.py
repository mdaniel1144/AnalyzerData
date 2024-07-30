from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import JSONResponse, StreamingResponse
from SqlDatabase import BuildDataBase, MakeQueryDataBase, SaveDatabaseToFile


app = FastAPI()


@app.post("/makeQuery")
async def MakeQuery(payload: dict):
    try:

        if 'listData' not in payload or 'query' not in payload:
            raise HTTPException(status_code=400, detail="Something is missing")

        listData = payload['listData']
        query = payload['query']
        
        print(f"-------------\nMake Query for You")
        conn = BuildDataBase(listData) # i want that i will return db , know he only save that
        results = MakeQueryDataBase(query , conn)
        conn.close()
        print("---------------------")
        print(results)
        return JSONResponse(status_code=200, content={"results":results})
    
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={'message': f"Failed to build database: {str(e.detail)}"})
    except Exception as e:
        print(f"-->Error in server:\n   {str(e)}")
        return JSONResponse(status_code=500, content={'message': f"{str(e)}"})
    
    
@app.post("/BuildDatabase")
async def BuildDatabase(payload: dict):
    try:

        if 'listData' not in payload:
            raise HTTPException(status_code=400, detail="Something is missing")

        listData = payload['listData']
        
        print(f"-------------\nMake File for You")
        conn = BuildDataBase(listData) # i want that i will return db , know he only save that
        db_bytes = SaveDatabaseToFile(conn)
        conn.close()
        print("---------------------")

        return StreamingResponse(db_bytes, media_type='application/sql', headers={'Content-Disposition': 'attachment; filename=database.sql'})

    
    except HTTPException as e:
        return JSONResponse(status_code=400,  content={'message': f"Error: {str(e.detail)}"})
    except Exception as e:
        print(f"-->Error in server:\n   {str(e)}")
        return JSONResponse(status_code=500,  content={'message': f"Error downloading database: {str(e)}"})