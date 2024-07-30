from typing import Optional
from pydantic import BaseModel 
import pandas as pd
from enum import Enum


class Relationship(Enum):
    OneToOne = "OneToOne"
    ManyToOne = "ManyToOne"
    ManyToMany = "ManyToMany"
    
class Column(BaseModel):
    name: str
    valueType: str
    
    def __str__(self):
        return self.name
    
    
class Summary(BaseModel):
    name: str
    count: str
    interstingCol: str
    interstingColDescription: dict
    graphCategory: list[str]
    graphNumric: list[str]


class Table(BaseModel):
    
    name: str
    size: list[int]
    primaryKey: str #Name of Col
    foreignKey: Optional[str] = None  # Name of the foreign key column, can be None
    reference: Optional[str] = None #name of table --> it must be exist and his primaryKey
    columns: list[Column]    
    rows: list
    is_readable: bool
    
    def __str__(self):
        return f"""--------Table - Name - {self.name}-------
        size: {self.size}
        primaryKey: {self.primaryKey}
        foreignKey: {self.foreignKey}
        reference: {self.reference}
        columns: {self.columns}
        rows: {len(self.rows)}
        is_readable: {self.is_readable}"""
    
    
    def to_dataframe(self):
        # Create a dictionary for the DataFrame
        data_dict = {}
        for col in self.columns:
            data_dict[col.name] = []

        # Populate dictionary with rows
        for row in self.rows:
            for col, value in zip(self.columns, row):
                data_dict[col.name].append(value)

        # Create DataFrame
        df = pd.DataFrame(data_dict)
        return df
    






