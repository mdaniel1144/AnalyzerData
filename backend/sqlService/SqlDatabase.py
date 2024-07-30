from config import TYPE_OF_SQL_INTEGER , TYPE_OF_SQL_STRING
from schemas import Table
import sqlite3
import io 


def BuildDataBase(listTable: list[dict]):
    try:
        conn = sqlite3.connect(':memory:')   #Connect to SQLite Database:
    
        for x in listTable:
        
            table = Table(**x)
            isHasLeagal = False
            sql_query = f"CREATE TABLE {table.name} ("
        
            for index in range(len(table.columns)):
                sql_query += "'"+table.columns[index].name+"'"
                if table.columns[index].valueType in TYPE_OF_SQL_INTEGER:
                    sql_query += " NUMERIC"
                if table.columns[index].valueType in TYPE_OF_SQL_STRING:
                    sql_query += " TEXT"
                if table.columns[index].name == table.primaryKey:
                    sql_query += " PRIMARY KEY"
                if index != len(table.columns)-1:
                    sql_query += ","

            if table.foreignKey != "":
                sql_query += ","
                for y in listTable:
                    table_2 = Table(**y)
                    if table_2 != table and table.foreignKey == table_2.primaryKey and table.reference == table_2.name:
                        sql_query += "FOREIGN KEY ("+table.foreignKey+") REFERENCES "+table.reference+"("+table.foreignKey+")"
                        isHasLeagal = True
                        break
            else:
                isHasLeagal = True
               
            if isHasLeagal == False:
                raise Exception(f"{table.name} can not be a database")
        
            sql_query += ")"
        
        
            df = table.to_dataframe()
            if(df[table.primaryKey].is_unique == False) :
                raise Exception(f"{table.name} can not be a database\n   {table.primaryKey} is not unique")
        
            if (table.foreignKey != "" and table.reference != ""):
                for t in listTable:
                    table_3 = Table(**t)
                    if table_3.name == table.reference and table.name != table_3.name:
                        df2 = table_3.to_dataframe()
                        if df2[table.foreignKey].is_unique == False:
                            raise Exception(f"{table.reference} can be a database\n   {table.foreignKey} is not unique")

        
            print(sql_query)
            conn.execute(sql_query)
            df.to_sql(table.name, conn, if_exists='replace', index=False)     #Create Customers table


        #Commit Changes and Close Connection:
        conn.commit()
        return conn
    
    except sqlite3.Error as e:
        raise e
    except Exception as e:
        raise e
    
    
def MakeQueryDataBase(query: str , conn: sqlite3.Connection):
    try:

        conn.row_factory = sqlite3.Row         # Set the row factory to sqlite3.Row

        cursor = conn.cursor()                          # Create a cursor object to interact with the database
        cursor.execute(query)                            # Execute a query
        rows = cursor.fetchall()                        #  Fetch all rows from the executed query

        results = [dict(row) for row in rows]           # Convert the rows to a list of dictionaries
        
        print(results)
        return results
        
    except sqlite3.Error as e:
        raise e
    except Exception as e:
        raise e
    
    
def SaveDatabaseToFile(conn: sqlite3.Connection):
    buffer = io.BytesIO()
    for line in conn.iterdump():
        buffer.write((line + '\n').encode('utf-8'))
    buffer.seek(0)
    return buffer