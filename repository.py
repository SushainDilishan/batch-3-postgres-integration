from typing import Optional, List

from psycopg2.extras import RealDictCursor

from database import get_db_connection
from models import BusRouteResponse, BusRouteCreate


class BusRouteRepository:

    def get_by_id(self, route_id) -> Optional[BusRouteResponse]:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        cursor.execute("SELECT * FROM bus_routes where id = %s;", (route_id,))
        route = cursor.fetchone()

        cursor.close()
        conn.close()

        return BusRouteResponse(**route) if route else None

    def get_all(self, offset: int = 0, limit: int = 20) -> List[BusRouteResponse]:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT * FROM bus_routes order by id ASC OFFSET %s LIMIT %s;", (offset,limit))

        routes = cursor.fetchall()

        cursor.close()
        conn.close()

        return [BusRouteResponse(**route) for route in routes]

    def create_bus_route(self, router_request: BusRouteCreate) -> Optional[BusRouteResponse]:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        query = """
        INSERT into bus_routes (route_number, start_location, end_location, bus_type, ticket_price)
        VALUES (%s, %s, %s, %s, %s) RETURNING * 
        """
        try:
            cursor.execute(query, (router_request.route_number
                                   , router_request.start_location
                                   , router_request.end_location
                                   , router_request.bus_type
                                   , router_request.ticket_price))

            inserted_record = cursor.fetchone()
            conn.commit()
            return BusRouteResponse(**inserted_record) if inserted_record else None
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    def delete_record(self, id):#delete from bus_routes where id = 2;

        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        query = """
        DELETE FROM bus_routes WHERE id = %s
        RETURNING *
        """

        try :
            cursor.execute(query,(id,))

            deleted_record = cursor.fetchone()

            conn.commit()

            return deleted_record is not None

        except Exception as e:
            conn.rollback()
            raise e

        finally:
            cursor.close()
            conn.close()








