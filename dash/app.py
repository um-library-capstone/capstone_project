from dash import Dash, html, __version__, page_container

app = Dash(__name__, use_pages=True)

app.layout = html.Main(
    [
        page_container,
    ]
)

if __name__ == "__main__":
    print(__version__)
    app.run(debug=True)