from typing import Optional, List

from starlette import status
from starlette.exceptions import HTTPException

from models import BusRouteResponse
from repository import BusRouteRepository


class BusRouteService:

    def __init__(self, repo: BusRouteRepository):
        self.repo = repo


    def get_bus_route_by_id(self, route_id) -> Optional[BusRouteResponse]:
        route = self.repo.get_by_id(route_id)

        if not route:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND
                                , detail='bus route not found')
        return route

    def get_all_routes(self, offset: int, limit: int) -> List[BusRouteResponse]:

        return self.repo.get_all(offset, limit)

    def create_bus_route(self, router_request) -> Optional[BusRouteResponse]:
        return self.repo.create_bus_route(router_request)