from typing import Optional, List

from psycopg2.extras import RealDictCursor

from database import get_db_connection
from models import BusRouteResponse, BusRouteCreate, BusRouteUpdate, ScheduleCreate, ScheduleResponse, \
    BusRoutesWithSchedules


class BusRouteRepository:


    def get_by_id_with_schedules(self, route_id) -> Optional[BusRoutesWithSchedules]:

        query = """
        select routes.id as route_id
                ,routes.route_number
                , routes.start_location
                , routes.end_location
                , routes.bus_type	
                , routes.ticket_price
                , sch.id as schedule_id
                , sch.departure_time
                , sch.arrival_time
                , sch.available_seats
                , sch.status
                from bus_routes routes
                left join schedules sch on sch.route_id = routes.id
                where routes.id = %s
                order by sch.departure_time asc nulls last;  
        """

        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        try:
            cursor.execute(query, (route_id,))
            rows = cursor.fetchall()
            if not rows:
                return None
            route = BusRoutesWithSchedules(
              id=rows[0]["route_id"],
              route_number=rows[0]["route_number"],
              start_location=rows[0]["start_location"],
              end_location=rows[0]["end_location"],
              bus_type=rows[0]["bus_type"],
              ticket_price=rows[0]["ticket_price"],
              schedules=[]
            )

            for row in rows:
                if row["schedule_id"] is not None:
                    route.schedules.append(
                        ScheduleResponse(
                            id=row["schedule_id"],
                            departure_time=row["departure_time"],
                            arrival_time=row["arrival_time"],
                            available_seats=row["available_seats"],
                            status=row["status"],
                            route_id=route_id
                        )
                    )
            return route
        except Exception as e:
            print(str(e))
        finally:
            cursor.close()
            conn.close()

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

    def update_by_id(self, route_id: int, route_update: BusRouteUpdate) -> Optional[BusRouteResponse]:

        query = """
        UPDATE bus_routes
        SET route_number = %s,
        start_location = %s,
        end_location = %s,
        bus_type = %s,
        ticket_price = %s
        WHERE id = %s
        RETURNING *  
        """
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        try:
            cursor.execute(query, (route_update.route_number
                                   , route_update.start_location
                                   ,route_update.end_location,
                                   route_update.bus_type,
                                   route_update.ticket_price,
                                   route_id))
            updated_rec = cursor.fetchone()
            conn.commit()
            return BusRouteResponse(**updated_rec) if updated_rec else None
        except Exception as e:
            conn.rollback()
            print(str(e))
        finally:
            cursor.close()
            conn.close()

class ScheduleRepository:

    def create(self, route_id: int, schedule_create: ScheduleCreate) -> Optional[ScheduleResponse]:
        query = """
        INSERT INTO schedules (route_id, departure_time, arrival_time, available_seats, status)
        VALUES (%s, %s::TIME, %s::TIME, %s, %s)
        RETURNING *
        """

        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        try:
            cursor.execute(query, (route_id
                                   , schedule_create.departure_time
                                   , schedule_create.arrival_time
                                   , schedule_create.available_seats
                                   , schedule_create.status))
            created_schedule = cursor.fetchone()
            conn.commit()
            if created_schedule:
                return ScheduleResponse(**{**created_schedule
                , "arrival_time": str(created_schedule["arrival_time"])
                , "departure_time": str(created_schedule["departure_time"])})
            return  None
        except Exception as e:
            conn.rollback()
            print(str(e))
        finally:
            cursor.close()
            conn.close()





