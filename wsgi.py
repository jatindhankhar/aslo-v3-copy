from aslo import init_app

application = init_app()

if __name__ == "__main__":
    host = '0.0.0.0'
    application.run(host=host)
