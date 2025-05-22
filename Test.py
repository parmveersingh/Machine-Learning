import pandas as pd
import networkx as nx
from dash import Dash, html, dcc, Input, Output, State, callback_context
import dash_cytoscape as cyto


cyto.load_extra_layouts()

external_css = ['/assets/graph.css']


app = Dash(__name__, external_stylesheets=external_css)

def create_enhanced_dash_app(file_path):
    
    original_df = pd.read_excel(file_path)
    original_df.columns = ['Source', 'Target']
    
    
    current_df = original_df.copy()
    G = nx.DiGraph()
    G.add_edges_from(zip(current_df['Source'], current_df['Target']))

    
    def create_elements(df):
        elements = []
        all_nodes = set(df['Source']).union(set(df['Target']))
        
        for node in all_nodes:
            node_color = '#a8e6cf' if str(node).lower().startswith('ingestion') else '#97c2fc'
            elements.append({
                'data': {'id': str(node), 'label': str(node)},
                'classes': 'rectangle',
                'style': {'background-color': node_color}
            })
        
        for _, row in df.iterrows():
            elements.append({
                'data': {'source': str(row['Source']), 'target': str(row['Target'])}
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

    
    app.layout = html.Div(style= {'font-family': 'Verdana,sans-serif', 'font-size': '15px' },children=[
        dcc.Store(id='original-data', data=original_df.to_dict('records')),
        html.Div(id='main-form', children=[
            html.H3("Graph Controls"),
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
            html.Button('Search', id='search-button', n_clicks=0),
            html.Button('Reset', id='reset-button', n_clicks=0),
            html.Div(id='search-status', style={'margin-top': '10px'}),
            html.Hr(),
            html.Label('Layout Algorithm:'),
            dcc.Dropdown(
                id='layout-dropdown',
                options=[
                    {'label': 'Hierarchical', 'value': 'dagre'},
                    {'label': 'Force-Directed', 'value': 'cose-bilkent'},
                    {'label': 'Grid', 'value': 'grid'},
                    {'label': 'Circle', 'value': 'circle'}
                ],
                value='dagre',
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
                marks={i/10: str(i/10) for i in range(1, 21, 2)},
                tooltip={'placement': 'bottom'}
            )
        ]),
        
        html.Div([
            cyto.Cytoscape(
                id='cytoscape',
                elements=create_elements(current_df),
                stylesheet=stylesheet,
                style={'width': '100%', 'height': '90vh'},
                layout={'name': 'dagre'},
                zoom=1
            )
        ], style={'width': '100%', 'display': 'inline-block', 'height': '90vh', 'position': 'relative'})
    ])

    
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
        
        
        full_df = pd.DataFrame(stored_data)
        G = nx.DiGraph()
        G.add_edges_from(zip(full_df['Source'], full_df['Target']))
        
        
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
         Output('search-status', 'children')],
        [Input('search-button', 'n_clicks'),
         Input('reset-button', 'n_clicks')],
        [State('search-input', 'value'),
         State('search-type-dropdown', 'value'),
         State('original-data', 'data')]
    )
    def update_graph(search_clicks, reset_clicks, search_term, search_type, stored_data):
        ctx = callback_context
        if not ctx.triggered:
            return create_elements(pd.DataFrame(stored_data)), "Showing full graph"
        
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        
        if button_id == 'reset-button':
            return create_elements(pd.DataFrame(stored_data)), "Showing full graph (reset)"
        
        if not search_term:
            return create_elements(pd.DataFrame(stored_data)), "Please enter a search term"
        
        # Convert stored data back to DataFrame
        full_df = pd.DataFrame(stored_data)
        G = nx.DiGraph()
        G.add_edges_from(zip(full_df['Source'], full_df['Target']))
        
        # Find exact match for the node
        matched_nodes = [node for node in G.nodes if str(node).lower() == search_term.lower()]
        
        if not matched_nodes:
            return create_elements(pd.DataFrame(columns=['Source', 'Target'])), f"Node not found: {search_term}"
        
        target_node = matched_nodes[0]
        related_nodes = set()
        edges_subset = set()

        if search_type == 'parents':
            # Get all ancestors
            related_nodes.update(nx.ancestors(G, target_node))
            related_nodes.add(target_node)
            
        elif search_type == 'children':
            # Get all descendants
            related_nodes.update(nx.descendants(G, target_node))
            related_nodes.add(target_node)
            
        elif search_type == 'immediate':
            # Get direct parents and children
            related_nodes.add(target_node)
            related_nodes.update(G.predecessors(target_node))
            related_nodes.update(G.successors(target_node))
            
        elif search_type == 'full':
            # Get entire connected component
            undirected_G = G.to_undirected()
            related_nodes.update(nx.node_connected_component(undirected_G, target_node))
        
        # Get all edges between related nodes
        connected_edges = full_df[
            (full_df['Source'].isin(related_nodes)) & 
            (full_df['Target'].isin(related_nodes))
        ]
        
        status_text = f"Showing {search_type.replace('-', ' ')} for: {search_term}"
        return create_elements(connected_edges), status_text

    
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

    return app

if __name__ == '__main__':
    app = create_enhanced_dash_app("dag_relationship.xlsx")
    app.run(debug=True)
