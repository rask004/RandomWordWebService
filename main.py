from bottle import default_app, run

from web_service.app import create_app

web_service = create_app()
web_service.run(host='0.0.0.0', port=5000)
