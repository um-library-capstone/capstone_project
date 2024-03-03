from dash import html, __version__, __version__, register_page

register_page(__name__, path="/")

layout = html.Div(className="page-container", children="HOME")
