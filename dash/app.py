from dash import Dash, html, dcc, __version__, page_container, page_registry, Output, Input, callback
from dash.exceptions import PreventUpdate
from pprint import pprint

app = Dash(__name__, use_pages=True)

options = []
for page in page_registry.values():
    label = {
        "Home": "Home Page",
        "Persona-1": "Persona One",
        "Persona-2": "Persona Two",
        "Persona-3": "Persona Three",
    }.get(page["name"], page["name"])
    options.append({"label": label, "value": page["path"]})


app.layout = html.Main(
    [
        html.Header(
            children=[
                dcc.Location(id="main-url", refresh=True),
                html.H1("Multi-page app with Dash Pages"),
                dcc.Dropdown(id="page-selector", options=options, placeholder="Select a Persona"),
            ]
        ),
        page_container,
    ]
)


@callback(Output(component_id="main-url", component_property="pathname"), Input("page-selector", "value"))
def update_page(path):
    if not path:
        raise PreventUpdate
    else:
        return path


if __name__ == "__main__":
    print(__version__)
    app.run(debug=True)
