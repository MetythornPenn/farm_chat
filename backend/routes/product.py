from fastapi import APIRouter, Depends, Response
from fastapi.response import StreamingResponse
from csv


from schemas.product import ProductSchema
from db.database import get_db
from services.product import ProductService

router = APIRouter()
