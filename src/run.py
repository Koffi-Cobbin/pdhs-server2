from pdhs_app import create_app

app = create_app(env='development')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
    # app.run()
