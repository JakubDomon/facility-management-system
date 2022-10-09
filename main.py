from website import create_app

# UTWORZENIE INSTANCJI
app = create_app()

# START APKI
if __name__ == '__main__':
    app.run(debug=True)