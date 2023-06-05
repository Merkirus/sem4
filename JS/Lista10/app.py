from textual.app import App, ComposeResult
from textual.containers import Container, VerticalScroll
from textual.widgets import DataTable, Header, Footer, Static, Label
import wrm_controller as ctrl

from sqlalchemy import create_engine
from create_database import DBMS_NAME, create_db
from load_data import df_to_db, load_csv_to_pd_df, read_csv_and_db_name_from_argv, path

AVRG_TIME_RENTAL_TEXT = "Average rental time as a rental station: "
AVRG_TIME_RETURN_TEXT = "Average rental time as a return station: "
NO_BIKES_TEXT = "Number of unique bikes on station: "
AVRG_TIME_BOTH_TEXT = "Average rental time as both rental and return station: "
NO_BIKES_BOTH_TEXT = "Number of rentals with same rental and return station: "


class WRM(App):
    CSS = "DataTable {height: 1fr}"
    CSS_PATH = "app.css"
    BINDINGS = [
        ("q", "quit", "Quit"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        with Container():
            yield DataTable(id="table")
        with Container(id="info"):
            yield Static(
                AVRG_TIME_RENTAL_TEXT, classes="info-item", id="avrg_time_rental"
            )
            yield Static(
                AVRG_TIME_RETURN_TEXT, classes="info-item", id="avrg_time_return"
            )
            yield Static(NO_BIKES_TEXT, classes="info-item", id="no_bikes")
            yield Static(AVRG_TIME_BOTH_TEXT, classes="info-item", id="avrg_time_both")
            yield Static(AVRG_TIME_BOTH_TEXT, classes="info-item", id="no_bikes_both")
        yield Footer()

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.focus()
        table.cursor_type = "row"
        table.add_columns(*COLUMN_NAMES)
        table.add_rows(ROWS)

    def on_data_table_row_selected(self) -> None:
        station_name = ROWS[self.query_one(DataTable).cursor_row][1]
        self.query_one("#avrg_time_rental", Static).update(
            AVRG_TIME_RENTAL_TEXT
            + str(
                ctrl.get_average_ride_time_on_rental_station(station_name, engine)
            ).split(".")[0]
        )
        self.query_one("#avrg_time_return", Static).update(
            AVRG_TIME_RETURN_TEXT
            + str(
                ctrl.get_average_ride_time_on_return_station(station_name, engine)
            ).split(".")[0]
        )
        self.query_one("#no_bikes", Static).update(
            NO_BIKES_TEXT
            + str(ctrl.get_bike_no_on_return_station(station_name, engine))
        )
        self.query_one("#avrg_time_both", Static).update(
            AVRG_TIME_BOTH_TEXT
            + str(
                ctrl.get_average_ride_time_for_bikes_with_same_stations(
                    station_name, engine
                )
            ).split(".")[0]
        )
        self.query_one("#no_bikes_both", Static).update(
            NO_BIKES_BOTH_TEXT
            + str(ctrl.get_no_bikes_with_same_stations(station_name, engine))
        )


app = WRM()
if __name__ == "__main__":
    db = "rentals"
    if not path.exists(db + ".db"):
        print("Database doesn't exist!")
    else:
        engine = create_engine(f"{DBMS_NAME}:///{db}.db")

        COLUMN_NAMES = ("station_number", "station_name")
        ROWS = ctrl.get_all_stations(engine)
        app.run()
