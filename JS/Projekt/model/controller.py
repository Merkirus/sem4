class Controller():
    def __init__(self, req, view) -> None:
        self.request = req
        self.view = view

        view.set_listener(self.send_request)

        self.view.run()

    def send_request(self):
        if not self.view.get_city_date():
            return

        self.view.update(self.request.get_json(self.view.get_city_date())
)

