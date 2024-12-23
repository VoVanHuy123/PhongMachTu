from app import create_app,db

app= create_app()

@app.template_filter('format_currency')
def format_currency(value):
    if value is None:
        return "0"
    return f"{value:,.0f}".replace(",", ".")


if __name__ == '__main__': 
    db.metadata.clear()
    app.run(debug=True)