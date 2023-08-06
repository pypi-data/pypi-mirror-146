try:
    from .plugins.webapp import build_app
    from .plugins.layout import *
except:
    from plugins.webapp import build_app
    from plugins.layout import *

import threading, webbrowser

url = '127.0.0.1'
port = '8051'
threading.Timer(1.25, lambda: webbrowser.open('http://' + url + ":" + port)).start()


# import socket
# socket.getaddrinfo('localhost', port)


def build_layout2():
    return html.Div(
        id="app-container",
        children=[
            build_dcc_store_card(),
            # Input
            build_input_card(),
            html.Br(),
            build_profile_card(),
            html.Br(),
            build_preprocess_card(),
            html.Br(),
            build_qc_card(),
            html.Br(),
            build_annotation_card(),
            html.Br(),
            html.Button('Phenotype association Analysis', id='run-button', n_clicks=0,
                        style={
                            'background-color': 'red',
                            'color': 'white',
                        }),
            html.Br(),
            build_diff_card(),
            html.Br(),
            build_decomposition_card(),
            html.Br(),
            build_clustering_card(),
            html.Br(),
            build_association_card(),
            html.Br(),
            build_enrich_card(),
            html.Br(),
            # build_genz_card(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),

        ]
    )


app = build_app()
app.layout = build_layout2()
app.run_server(host=url, port=port)
