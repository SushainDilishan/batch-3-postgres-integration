from typing import Optional

from fastapi import APIRouter

from models import BusRouteResponse, BusRouteCreate, BusRouteUpdate
from repository import BusRouteRepository
from services import BusRouteService

router = APIRouter(prefix="/routes")

service = BusRouteService(repo=BusRouteRepository())


@router.get("/{route_id}", response_model=Optional[BusRouteResponse]) #Path variable
def get_by_id(route_id: int):
    return service.get_bus_route_by_id(route_id)


@router.get("/")
def get_all(offset: int = 0 , limit: int = 10): #Query parameters
    return service.get_all_routes(offset, limit)


@router.post("/", response_model=BusRouteResponse, status_code=201)
def create_bus_route(router_request: BusRouteCreate):
    return service.create_bus_route(router_request)

@router.delete("/{id}",status_code=200)
def delete_bus_route(id):
    return  service.delete_bus_record(id)

@router.put("/{route_ud}", response_model=BusRouteResponse)
def update_route(route_id, update_req: BusRouteUpdate):
    return service.update_route(route_id, update_req)