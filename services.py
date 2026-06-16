from typing import Optional, List

from starlette import status
from starlette.exceptions import HTTPException

from models import BusRouteResponse, BusRouteUpdate
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
        try:
            return self.repo.create_bus_route(router_request)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to create record + {str(e)}")

    def delete_bus_record(self,id) :

        try:
            return self.repo.delete_record(id)

        except Exception as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Record not found + {e}")

    def update_route(self, route_id: int, update_request: BusRouteUpdate) -> Optional[BusRouteResponse]:

        try:
            updated_rec = self.repo.update_by_id(route_id, update_request)

            if not updated_rec:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found to update")

            return updated_rec
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Server Error {str(e)}")