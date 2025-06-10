import polars as pl
import networkx as nx
from dash import Dash, html, dcc, Input, Output, State, callback_context, no_update, clientside_callback
import dash_cytoscape as cyto

cyto.load_extra_layouts()

external_css = ['/assets/graph.css']

app = Dash(__name__, external_stylesheets=external_css)


def create_enhanced_dash_app(file_path):
    original_df = pl.read_excel(file_path)
    current_df = original_df.clone()
    G = nx.DiGraph()

    G.add_edges_from(current_df.rows())

    def create_elements(df):
        elements = []
        all_nodes = set(df["Source"].to_list() + df["Target"].to_list())

        for node in all_nodes:
            node_color = '#a8e6cf' if str(node).lower().startswith('ingestion') else '#97c2fc'
            elements.append({
                'data': {'id': str(node), 'label': str(node)},
                'classes': 'rectangle',
                'style': {'background-color': node_color}
            })

        for row in df.rows():
            source, target = row
            elements.append({
                'data': {'source': str(source), 'target': str(target)}
            })

        return elements

    stylesheet = [
        {
            'selector': 'node',
            'style': {
                'content': 'data(label)',
                'text-valign': 'center',
                'text-halign': 'center',
                'shape': 'round-rectangle',
                'background-color': 'data(background-color)',
                'border-color': '#2b7ce9',
                'border-width': 2,
                'width': 'label',
                'height': 'label',
                'padding': '10px',
                'text-wrap': 'wrap',
                'text-max-width': '100px',
                'border-radius': '10px'
            }
        },
        {
            'selector': 'node[background-color = "#a8e6cf"]',
            'style': {
                'border-color': '#4CAF50',
                'border-width': 3
            }
        },
        {
            'selector': 'edge',
            'style': {
                'curve-style': 'bezier',
                'target-arrow-shape': 'triangle',
                'arrow-scale': 1.5,
                'width': 1,
                'line-color': '#9dbaea',
                'target-arrow-color': '#9dbaea'
            }
        },
        {
            'selector': ':selected',
            'style': {
                'background-color': '#ff4136',
                'line-color': '#ff4136',
                'target-arrow-color': '#ff4136',
                'source-arrow-color': '#ff4136'
            }
        }
    ]

    app.layout = html.Div(style={'font-family': 'Verdana,sans-serif', 'font-size': '15px'}, children=[
        dcc.Store(id='original-data', data=original_df.to_dict(as_series=False)),
        dcc.Store(id='initial-state', data={'searched': False}),
        dcc.Location(id='url', refresh=True),


        html.Div(
            id='alert-dialog',
            children=[
                html.Div(
                    [
                        html.H3("Alert", style={'margin-top': '0', 'color': '#2b7ce9'}),
                        html.Div(id='alert-message', style={'margin': '20px 0'}),
                        html.Button(
                            'OK',
                            id='alert-ok-button',
                            n_clicks=0,
                            style={
                                'background-color': '#2b7ce9',
                                'color': 'white',
                                'border': 'none',
                                'padding': '10px 20px',
                                'border-radius': '5px',
                                'cursor': 'pointer',
                                'font-size': '15px'
                            }
                        )
                    ],
                    style={
                        'background-color': 'white',
                        'padding': '20px',
                        'border-radius': '10px',
                        'box-shadow': '0 4px 8px rgba(0,0,0,0.2)',
                        'text-align': 'center',
                        'width': '300px'
                    }
                )
            ],
            style={
                'position': 'fixed',
                'top': '0',
                'left': '0',
                'width': '100%',
                'height': '100%',
                'background-color': 'rgba(0,0,0,0.5)',
                'display': 'flex',
                'justify-content': 'center',
                'align-items': 'center',
                'z-index': '100000',
                'display': 'none'
            }
        ),


        html.Div(id='main-form', children=[
            html.H3("DAG Search"),
            html.Label('Search Type:'),
            dcc.Dropdown(
                id='search-type-dropdown',
                options=[
                    {'label': 'Search Parents', 'value': 'parents'},
                    {'label': 'Search Children', 'value': 'children'},
                    {'label': 'Search Immediate Members', 'value': 'immediate'},
                    {'label': 'Search Full Tree', 'value': 'full'}
                ],
                value='full',
                clearable=False,
                style={'width': '100%'}
            ),
            html.Label('Search Node:'),
            dcc.Input(
                id='search-input',
                type='text',
                placeholder='Enter node name...'
            ),

            html.Div([
                html.Button('Search', id='search-button', n_clicks=0,
                            style={'width': '48%', 'margin-right': '4%'}),
                html.Button('Reset', id='reset-button', n_clicks=0,
                            style={'display': 'none', 'width': '48%'})
            ], style={'display': 'flex', 'justify-content': 'space-between'}),

            html.Div(id='search-status', style={'margin-top': '10px'}),


            html.Div(id='layout-controls', children=[
                html.Hr(),
                html.Label('Layout Algorithm:'),
                dcc.Dropdown(
                    id='layout-dropdown',
                    options=[
                        {'label': 'Grid', 'value': 'grid'},
                        {'label': 'Hierarchical', 'value': 'dagre'},
                        {'label': 'Force-Directed', 'value': 'cose-bilkent'},
                        {'label': 'Circle', 'value': 'circle'}
                    ],
                    value='grid',
                    clearable=False,
                    style={'width': '100%'}
                ),
                html.Label('Zoom Level:'),
                dcc.Slider(
                    id='zoom-slider',
                    min=0.1,
                    max=2,
                    step=0.1,
                    value=1,
                    marks={i / 10: str(i / 10) for i in range(1, 21, 2)},
                    tooltip={'placement': 'bottom'}
                )
            ], style={'display': 'none'})
        ], style={
            'position': 'fixed',
            'top': '50%',
            'left': '50%',
            'transform': 'translate(-50%, -50%)',
            'padding': '20px',
            'background-color': '#97c2fc47',
            'border-radius': '10px',
            'z-index': '99999',
            'transition': 'all 0.5s ease'
        }),


        html.Div(id='graph-container', children=[
            cyto.Cytoscape(
                id='cytoscape',
                elements=create_elements(current_df),
                stylesheet=stylesheet,
                style={'width': '100%', 'height': '90vh'},
                layout={'name': 'grid'},
                zoom=1
            )
        ], style={'display': 'none', 'width': '100%', 'height': '90vh'})
    ])

    @app.callback(
        [Output('main-form', 'style'),
         Output('graph-container', 'style'),
         Output('layout-controls', 'style'),
         Output('initial-state', 'data'),
         Output('reset-button', 'style'),
         Output('search-input', 'value')],
        [Input('search-button', 'n_clicks'),
         Input('reset-button', 'n_clicks')],
        [State('initial-state', 'data'),
         State('search-input', 'value')]
    )
    def handle_ui_transition(search_clicks, reset_clicks, state, search_term):
        ctx = callback_context
        if not ctx.triggered:
            return no_update, no_update, no_update, no_update, no_update, no_update

        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if button_id == 'reset-button' or not search_term:
            return (
                {
                    'position': 'fixed',
                    'top': '50%',
                    'left': '50%',
                    'transform': 'translate(-50%, -50%)',
                    'padding': '20px',
                    'background-color': '#97c2fc47',
                    'border-radius': '10px',
                    'z-index': '99999',
                    'transition': 'all 0.5s ease'
                },
                {'display': 'none', 'width': '100%', 'height': '90vh'},
                {'display': 'none'},
                {'searched': False},
                {'display': 'none', 'width': '48%'},
                ''
            )

        elif button_id == 'search-button' and search_term:
            return (
                {
                    'width': '20%',
                    'padding': '20px',
                    'background-color': '#97c2fc47',
                    'bottom': '10px',
                    'left': '10px',
                    'position': 'absolute',
                    'border-radius': '10px',
                    'z-index': '99999',
                    'transition': 'all 0.5s ease'
                },
                {'display': 'block', 'width': '100%', 'height': '90vh'},
                {'display': 'block'},
                {'searched': True},
                {'display': 'block', 'width': '48%'},
                search_term
            )

        return no_update, no_update, no_update, state, no_update, no_update

    @app.callback(
        Output('cytoscape', 'stylesheet'),
        [Input('cytoscape', 'tapNode'),
         Input('reset-button', 'n_clicks')],
        [State('original-data', 'data')]
    )
    def highlight_parents(tap_node, reset_clicks, stored_data):
        ctx = callback_context
        if not ctx.triggered or ctx.triggered[0]['prop_id'] == 'reset-button.n_clicks':
            return stylesheet

        if not tap_node:
            return stylesheet

        full_df = pl.DataFrame(stored_data)
        G = nx.DiGraph()
        G.add_edges_from(full_df.rows())

        selected_node = tap_node['data']['id']
        ancestors = set()
        path_edges = set()

        def get_parents_and_edges(node):
            for predecessor in G.predecessors(node):
                edge = (predecessor, node)
                if edge not in path_edges:
                    path_edges.add(edge)
                    ancestors.add(predecessor)
                    get_parents_and_edges(predecessor)

        get_parents_and_edges(selected_node)

        dynamic_stylesheet = stylesheet.copy()

        dynamic_stylesheet.append({
            'selector': f'node[id = "{selected_node}"]',
            'style': {
                'background-color': '#ff4136',
                'border-color': '#ff0000',
                'border-width': 3,
                'z-index': 9999
            }
        })

        for ancestor in ancestors:
            dynamic_stylesheet.append({
                'selector': f'node[id = "{ancestor}"]',
                'style': {
                    'background-color': '#ffcc00',
                    'border-color': '#ff9900',
                    'border-width': 3,
                    'z-index': 9998
                }
            })

        for edge in path_edges:
            source, target = edge
            dynamic_stylesheet.append({
                'selector': f'edge[source = "{source}"][target = "{target}"]',
                'style': {
                    'line-color': '#ff9900',
                    'target-arrow-color': '#ff9900',
                    'width': 3
                }
            })

        return dynamic_stylesheet

    @app.callback(
        [Output('cytoscape', 'elements'),
         Output('search-status', 'children'),
         Output('alert-dialog', 'style'),
         Output('alert-message', 'children')],
        [Input('search-button', 'n_clicks'),
         Input('reset-button', 'n_clicks')],
        [State('search-input', 'value'),
         State('search-type-dropdown', 'value'),
         State('original-data', 'data')]
    )
    def update_graph(search_clicks, reset_clicks, search_term, search_type, stored_data):
        ctx = callback_context
        if not ctx.triggered:
            return create_elements(pl.DataFrame(stored_data)), "", no_update, no_update

        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if button_id == 'reset-button':
            return create_elements(pl.DataFrame(stored_data)), "", no_update, no_update

        if not search_term:
            return create_elements(pl.DataFrame(stored_data)), "Please enter a search term", no_update, no_update

        full_df = pl.DataFrame(stored_data)
        G = nx.DiGraph()
        G.add_edges_from(full_df.rows())

        matched_nodes = [node for node in G.nodes if str(node).lower() == search_term.lower()]

        if not matched_nodes:
            alert_style = {
                'position': 'fixed',
                'top': '0',
                'left': '0',
                'width': '100%',
                'height': '100%',
                'background-color': 'rgba(0,0,0,0.5)',
                'display': 'flex',
                'justify-content': 'center',
                'align-items': 'center',
                'z-index': '100000'
            }
            return ([], f"DAG not found: {search_term}",
                    alert_style,
                    f"DAG not found: {search_term}")

        target_node = matched_nodes[0]
        related_nodes = set()
        edges_subset = set()

        if search_type == 'parents':
            related_nodes.update(nx.ancestors(G, target_node))
            related_nodes.add(target_node)

        elif search_type == 'children':
            related_nodes.update(nx.descendants(G, target_node))
            related_nodes.add(target_node)

        elif search_type == 'immediate':
            related_nodes.add(target_node)
            related_nodes.update(G.predecessors(target_node))
            related_nodes.update(G.successors(target_node))

        elif search_type == 'full':
            undirected_G = G.to_undirected()
            related_nodes.update(nx.node_connected_component(undirected_G, target_node))

        connected_edges = full_df.filter(
            (pl.col("Source").is_in(related_nodes)) &
            (pl.col("Target").is_in(related_nodes))
        )

        if len(related_nodes) == 1 and connected_edges.is_empty():
            alert_style = {
                'position': 'fixed',
                'top': '0',
                'left': '0',
                'width': '100%',
                'height': '100%',
                'background-color': 'rgba(0,0,0,0.5)',
                'display': 'flex',
                'justify-content': 'center',
                'align-items': 'center',
                'z-index': '100000'
            }
            return ([], f"No {search_type} for {search_term}",
                    alert_style,
                    f"No {search_type} for {search_term}")

        status_text = f"Showing {search_type.replace('-', ' ')} for: {search_term}"
        return create_elements(connected_edges), status_text, no_update, no_update

    @app.callback(
        Output('url', 'refresh'),
        [Input('alert-ok-button', 'n_clicks')],
        prevent_initial_call=True
    )
    def refresh_on_ok(n_clicks):
        if n_clicks:
            return True
        return no_update

    @app.callback(
        Output('cytoscape', 'layout'),
        Input('layout-dropdown', 'value')
    )
    def update_layout(layout_value):
        return {'name': layout_value, 'animate': True}

    @app.callback(
        Output('cytoscape', 'zoom'),
        Input('zoom-slider', 'value')
    )
    def update_zoom(zoom_value):
        return zoom_value

    app.clientside_callback(
        """
        function(n_clicks) {
            if (n_clicks > 0) {
                document.getElementById('alert-dialog').style.display = 'none';
                setTimeout(function() {
                    window.location.reload();
                }, 100);
            }
            return window.dash_clientside.no_update;
        }
        """,
        Output('alert-ok-button', 'n_clicks'),
        Input('alert-ok-button', 'n_clicks')
    )

    return app


if __name__ == '__main__':
    app = create_enhanced_dash_app("dag_relationship.xlsx")
    app.run(debug=True)
