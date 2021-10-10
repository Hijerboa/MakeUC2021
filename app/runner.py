from server.server import get_app
import db.database_connection as dbc

if __name__ == '__main__':
    dbc.initialize()
    get_app().run_server(debug=True, host='0.0.0.0')