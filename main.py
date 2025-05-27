from website import create_app
app = create_app()
if __name__ == '__main__':
    app.run(debug=True) # debug=True will reload the server when you make changes to the code