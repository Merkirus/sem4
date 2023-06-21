import controller
import req
import view

if __name__ == "__main__":
    request = req.Request()
    view = view.GUI()
    controller = controller.Controller(request, view)

