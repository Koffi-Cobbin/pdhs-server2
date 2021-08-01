from src.pdhs_app.app import create_app

app = create_app(env='development')

if __name__ == '__main__':
    app.run()
