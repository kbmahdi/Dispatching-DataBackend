import numpy as np
from fastapi import APIRouter, HTTPException, Request, FastAPI, Body
import pandas as pd
from app.services.comboboxData import prepare_dropdown_data
from pydantic import BaseModel
from typing import List, Optional
from app.services.tableData import read_csv_to_list, parse_date_range, count_non_sunday_days
from app.services.tableData import calculate_metrics, calculate_metrics2
from app.services.tableData import calculate_store_metrics, calculate_store_metrics2, selected_canal_table_multiple_stores
from app.services.filtering_service import get_filtered_data
from datetime import datetime, timedelta
import json

router = APIRouter()

csv_file_path = 'app/data/dataFinale.csv'


class StockCoverage(BaseModel):
    desiredStockCoverage: int


class BoutiqueKey(BaseModel):
    boutiqueName: str  # Add this line: int


class FilterModel(BaseModel):
    Boutique: Optional[List[int]] = None
    Date: Optional[List[str]] = None
    Categorie: Optional[List[str]] = None
    SousCat: Optional[List[str]] = None
    NomArticle: Optional[List[str]] = None
    NewRework: Optional[List[str]] = None


class SelectedValues(BaseModel):
    canal: str
    store: str
    categorie: str
    sousCat: str
    nomArticle: str
    newRework: str
    date_range_str: str


class DateRange(BaseModel):
    date_range_str: str


class SelectedCanalRequestBody(BaseModel):
    store_names: List[str]
    desired_stock_coverage: float
    date_range_str: str  # Assuming date_range is a dictionary as per your latest update


class Item(BaseModel):
    VentePS: float
    BesoinNew: float
    BesoinNewSouhaite: str
    RemplacementPS: int
    BesoinRework: int
    BesoinReworkSouhaite: int


@router.get("/read-csv")
async def read_csv_file():
    # Read the CSV file using Pandas
    df = pd.read_csv(csv_file_path)

    # Replace NaN values with None
    df.fillna(value=np.nan, inplace=True)

    # Display the first 5 rows of the DataFrame
    first_five_rows = df.head(50).to_dict('records')

    return first_five_rows


@router.get("/read-combobox")
async def read_combobox():
    try:
        # No need to specify csv_file_path here as it's globally available
        data = prepare_dropdown_data()
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/list")
async def read_list():
    try:
        # No need to specify csv_file_path here as it's globally available
        data = read_csv_to_list()
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/somme")
async def calculate_sommes(date_range: DateRange):
    try:
        data = calculate_metrics(csv_file_path, date_range.date_range_str)
        data2 = calculate_store_metrics(csv_file_path, date_range.date_range_str)
        result = {
            'total': data,
            'indiv': data2
        }
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/testdate")
async def seeDate(date_range: DateRange):
    try:
        non_sunday_days = count_non_sunday_days(date_range.date_range_str)
        return {"non_sunday_days": non_sunday_days}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/stock-coverage")
async def update_stock_coverage(body: StockCoverage = Body(...)):
    print(body.desiredStockCoverage)
    # Your logic here
    return {"received_stock_coverage": body.desiredStockCoverage}




@router.post("/checkedBoutique")
async def receive_boutique_key(body: BoutiqueKey = Body(...)):
    print(body.boutiqueName)
    return body.boutiqueName


@router.post("/selected-canal-table")
async def get_selected_canal_table(body: SelectedCanalRequestBody):
    try:
        # Now body.store_names is a list of store names
        store_names = body.store_names
        desired_stock_coverage = body.desired_stock_coverage
        date_range_str = body.date_range_str

        # Adjust the call to selected_canal_table to pass the list of store names
        results = selected_canal_table_multiple_stores(store_names, desired_stock_coverage, date_range_str)
        print(date_range_str)
        print(results)

        # Return the results as a list of dictionaries
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

'''
@router.get("/testtest", response_model=dict)
async def read_combobox2(selected_canal: Optional[str] = None):
    try:
        data = prepare_dropdown_data2(selected_canal)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
'''


@router.post("/send-selected-filters")
async def receive_selected_values(selected_values: SelectedValues = Body(...)):

    date_range_str = selected_values.date_range_str
    print(date_range_str)

    # Split the canal string into a list of names
    canal_names = selected_values.canal.split(', ')
    store_names = selected_values.store.split(', ')
    categorie_names = selected_values.categorie.split(', ')
    sousCat_names = selected_values.sousCat.split(', ')
    nomArticle_names = selected_values.nomArticle.split(', ')
    newRework_names = selected_values.newRework.split(', ')

    allData=selected_values

    print(canal_names)
    print(store_names)
    print(categorie_names)
    print(sousCat_names)
    print(nomArticle_names)
    print(newRework_names)

    print(allData)

    canal = selected_values.canal
    store=selected_values.store
    categorie=selected_values.categorie
    sousCat=selected_values.sousCat
    nomArticle=selected_values.nomArticle
    newRework=selected_values.newRework

    # Call calculate_metrics with the canal value
    data = calculate_metrics2(csv_file_path, date_range_str, canal=canal, store=store, categorie=categorie, sousCat=sousCat, nomArticle=nomArticle, newRework=newRework)
    data2=calculate_store_metrics2(csv_file_path, date_range_str, canal=canal, store=store, categorie=categorie, sousCat=sousCat, nomArticle=nomArticle, newRework=newRework)
    result = {
        'total': data,
        'indiv': data2
    }

    return result


''' new new
router.post("/send-selected-filters")
async def receive_selected_values(selected_values: SelectedValues = Body(...)):
    # Split the canal string into a list of names
    canal_names = selected_values.canal.split(', ')
    store_names = selected_values.store.split(', ')
    categorie_names = selected_values.categorie.split(', ')
    sousCat_names = selected_values.sousCat.split(', ')
    nomArticle_names = selected_values.nomArticle.split(', ')
    newRework_names = selected_values.newRework.split(', ')

    allData=selected_values

    print(canal_names)
    print(store_names)
    print(categorie_names)
    print(sousCat_names)
    print(nomArticle_names)
    print(newRework_names)

    print(allData)

    # Prepare the data with the selected canal filter
    dropdown_data = prepare_dropdown_data2(
        canal_filter=selected_values.canal,
        category_filter=selected_values.categorie,
        subcategory_filter=selected_values.sousCat
    )

    return {"status": "success", "dropdown_data": dropdown_data}
'''


@router.post("/dispatching-table-data")
async def receive_table_data(data: List[dict]):
    # Process the received data
    for item in data:
        print(item)
        # Perform operations with each item, such as saving to database or processing further
    return {"status": "success"}

