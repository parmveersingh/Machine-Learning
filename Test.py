import pandas as pd
import networkx as nx
from dash import Dash, html, dcc, Input, Output, State, callback_context
import dash_cytoscape as cyto

# Load required Cytoscape extensions
cyto.load_extra_layouts()

# Initialize the Dash app
app = Dash(__name__)

def create_enhanced_dash_app(file_path):
    # Read and store original data
    original_df = pd.read_excel(file_path)
    original_df.columns = ['parent', 'child']  # Ensure consistent column names
    
    # Initialize with full data
    current_df = original_df.copy()
    G = nx.DiGraph()
    G.add_edges_from(zip(current_df['parent'], current_df['child']))

    # Convert to Cytoscape elements
    def create_elements(df):
        elements = []
        all_nodes = set(df['parent']).union(set(df['child']))
        
        for node in all_nodes:
            node_color = '#a8e6cf' if str(node).lower().startswith('ingestion') else '#97c2fc'
            elements.append({
                'data': {'id': str(node), 'label': str(node)},
                'classes': 'rectangle',
                'style': {'background-color': node_color}
            })
        
        for _, row in df.iterrows():
            elements.append({
                'data': {'source': str(row['parent']), 'target': str(row['child'])}
            })
        
        return elements

    # Define stylesheet with rounded corners
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

    # App layout with search functionality
    app.layout = html.Div([
        dcc.Store(id='original-data', data=original_df.to_dict('records')),
        html.Div([
            html.H3("Graph Controls"),
            html.Label('Search Node (Parent or Child):'),
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
                    {'label': 'Hierarchical (Dagre)', 'value': 'dagre'},
                    {'label': 'Force-Directed (CoSE)', 'value': 'cose-bilkent'},
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

    # Callback for search functionality
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
        
        # Convert stored data back to DataFrame
        full_df = pd.DataFrame(stored_data)
        
        # Find all rows where parent or child contains the search term (case insensitive)
        mask = (full_df['parent'].astype(str).str.lower().str.contains(search_term.lower())) | \
               (full_df['child'].astype(str).str.lower().str.contains(search_term.lower()))
        
        filtered_df = full_df[mask]
        
        if filtered_df.empty:
            return create_elements(pd.DataFrame(columns=['parent', 'child'])), f"No matches found for: {search_term}"
        
        # Get all unique nodes in filtered results
        all_nodes = set(filtered_df['parent']).union(set(filtered_df['child']))
        
        # Find all edges that connect these nodes (upstream and downstream)
        connected_edges = full_df[
            (full_df['parent'].isin(all_nodes)) | 
            (full_df['child'].isin(all_nodes))
        ]
        
        return create_elements(connected_edges), f"Showing results for: {search_term}"

    # Existing layout and zoom callbacks
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
    app = create_enhanced_dash_app("parent_child_data.xlsx")
    app.run(debug=True)
