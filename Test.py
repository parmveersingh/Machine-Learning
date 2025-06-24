from dash.exceptions import PreventUpdate



        html.Div(id='graph-container', children=[
            html.Div(
                id='download-container',
                children=[
                    html.Button(
                        [
                            html.Img(
                                src=f"/assets/download_icon.png",
                                style={
                                    'width': '16px',
                                    'height': '16px',
                                    'margin-right': '8px',
                                    'filter': 'invert(100%)'
                                }
                            ),
                            " Export Nodes"
                        ],
                        id='download-button',
                        n_clicks=0,
                        style={
                            'position': 'absolute',
                            'top': '15px',
                            'right': '15px',
                            'zIndex': 10000,
                            'display': 'flex',
                            'align-items': 'center',
                            'gap': '8px',
                        }
                    ),
                    dcc.Download(id="download-nodes")
                ],
                style={'position': 'absolute', 'top': '0', 'right': '0', 'zIndex': 10000}
            ),
            cyto.Cytoscape(
                id='cytoscape',
                elements=create_elements(current_df),
                stylesheet=stylesheet,
                style={'width': '100%', 'height': '90vh'},
                layout={'name': 'grid'},
                zoom=1
            )
        ], style={'display': 'none', 'width': '100%', 'height': '90vh', 'position': 'relative'})
    ])

   
    @app.callback(
        Output('download-nodes', 'data'),
        [Input('download-button', 'n_clicks')],
        [State('cytoscape', 'elements')]
    )
    def download_nodes(n_clicks, elements):
        if n_clicks is None or n_clicks == 0:
            raise PreventUpdate

        nodes = [elem for elem in elements if 'source' not in elem['data']]
        node_labels = [node['data']['label'] for node in nodes]

        if not node_labels:
            raise PreventUpdate

        csv_content = "Node Name\n" + "\n".join(node_labels)

        return dict(content=csv_content, filename="nodes_list.csv")


    
    
    #download-button {
    background-color: #2b7ce9;
    color: white;
    border: none;
    padding: 10px 15px;
    border-radius: 5px;
    cursor: pointer;
    font-size: 15px;
    font-family: Verdana, sans-serif;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    justify-content: center;
}

#download-button:hover {
    background-color: #1a5cb0;
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}

#download-button:active {
    transform: translateY(0);
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}

