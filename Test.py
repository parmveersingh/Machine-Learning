import pandas as pd
import networkx as nx
from dash import Dash, html, dcc, Input, Output, State, callback_context
import dash_cytoscape as cyto


cyto.load_extra_layouts()


app = Dash(__name__)

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

    
    app.layout = html.Div([
        dcc.Store(id='original-data', data=original_df.to_dict('records')),
        html.Div([
            html.H3("Graph Controls"),
            html.Label('Search DAG Name:'),
            dcc.Input(
                id='search-input',
                type='text',
                placeholder='Enter search term...',
                style={'width': '100%'}
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
            html.Br(),
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
        ], style={'width': '20%', 'display': 'inline-block', 'padding': '20px'}),
        
        html.Div([
            cyto.Cytoscape(
                id='cytoscape',
                elements=create_elements(current_df),
                stylesheet=stylesheet,
                style={'width': '100%', 'height': '90vh'},
                layout={'name': 'dagre'},
                zoom=1
            )
        ], style={'width': '75%', 'display': 'inline-block', 'height': '90vh'})
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
         State('original-data', 'data')]
    )
    def update_graph(search_clicks, reset_clicks, search_term, stored_data):
        ctx = callback_context
        if not ctx.triggered:
            return create_elements(pd.DataFrame(stored_data)), "Showing full graph"
        
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        
        if button_id == 'reset-button':
            return create_elements(pd.DataFrame(stored_data)), "Showing full graph (reset)"
        
        if not search_term:
            return create_elements(pd.DataFrame(stored_data)), "Please enter a search term"
        
        
        full_df = pd.DataFrame(stored_data)
        
        
        G = nx.DiGraph()
        G.add_edges_from(zip(full_df['Source'], full_df['Target']))
        
        
        matched_nodes = [node for node in G.nodes if search_term.lower() in str(node).lower()]
        
        if not matched_nodes:
            return create_elements(pd.DataFrame(columns=['Source', 'Target'])), f"No matches found for: {search_term}"
        
        
        def get_all_related_nodes_dfs(graph, start_nodes):
            visited = set()
            stack = list(start_nodes)
            visited.update(stack)
            while stack:
                node = stack.pop()
                
                for neighbor in list(graph.successors(node)) + list(graph.predecessors(node)):
                    if neighbor not in visited:
                        visited.add(neighbor)
                        stack.append(neighbor)
            return visited
        
        all_related_nodes = get_all_related_nodes_dfs(G, matched_nodes)
        
        
        connected_edges = full_df[
            (full_df['Source'].isin(all_related_nodes)) & 
            (full_df['Target'].isin(all_related_nodes))
        ]
        
        return create_elements(connected_edges), f"Showing results for: {search_term}"

    
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
