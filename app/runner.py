from server.server import get_app

if __name__ == '__main__':
    get_app().run_server(debug=True)