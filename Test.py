import pandas as pd
import networkx as nx
from dash import Dash, html, dcc, Input, Output
import dash_cytoscape as cyto

# Load required Cytoscape extensions
cyto.load_extra_layouts()  # This loads additional layouts including dagre

# Initialize the Dash app
app = Dash(__name__)

def create_enhanced_dash_app(file_path):
    # Read data
    df = pd.read_excel(file_path)
    G = nx.DiGraph()
    G.add_edges_from(zip(df.iloc[:, 0], df.iloc[:, 1]))

    # Convert to Cytoscape elements
    elements = []
    for node in G.nodes():
        node_color = '#a8e6cf' if str(node).lower().startswith('ingestion') else '#97c2fc'
        elements.append({
            'data': {'id': str(node), 'label': str(node)},
            'classes': 'rectangle',
            'style': {'background-color': node_color}
        })
    
    for edge in G.edges():
        elements.append({
            'data': {'source': str(edge[0]), 'target': str(edge[1])}  # String IDs
        })

    # Define stylesheet
    stylesheet = [
        {
            'selector': 'node',
            'style': {
                'content': 'data(label)',
                'text-valign': 'center',
                'text-halign': 'center',
                'shape': 'round-rectangle',
                'background-color': 'data(background-color)',
                'border-color': 'data(background-color)',
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
            'selector': 'node[background-color = "#a8e6cf"]',  # Special style for ingestion nodes
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
        },
        {
            'selector': '.highlighted',
            'style': {
                'background-color': '#FFD700',
                'line-color': '#FFD700',
                'target-arrow-color': '#FFD700',
                'transition-property': 'background-color, line-color',
                'transition-duration': '0.5s'
            }
        }
    ]

    # Set app layout with improved controls
    app.layout = html.Div([
        html.Div([
            html.H3("Graph Controls"),
            html.Label('Layout Algorithm:'),
            dcc.Dropdown(
                id='layout-dropdown',
                options=[
                    {'label': 'Hierarchical (Dagre)', 'value': 'dagre'},
                    {'label': 'Force-Directed (CoSE)', 'value': 'cose-bilkent'},
                    {'label': 'Grid', 'value': 'grid'},
                    {'label': 'Circle', 'value': 'circle'},
                    {'label': 'Breadthfirst', 'value': 'breadthfirst'},
                    {'label': 'Concentric', 'value': 'concentric'}
                ],
                value='dagre',
                clearable=False
            ),
            html.Br(),
            html.Label('Zoom Level:'),
            dcc.Slider(
                id='zoom-slider',
                min=0.1,
                max=2,
                step=0.1,
                value=1,
                marks={i/10: str(i/10) for i in range(1, 21, 2)}
            ),
            html.Br(),
            html.Label('Node Spacing:'),
            dcc.Slider(
                id='spacing-slider',
                min=10,
                max=200,
                step=10,
                value=50,
                marks={i: str(i) for i in range(10, 201, 20)}
            ),
            html.Br(),
            html.Label('Search Node:'),
            dcc.Input(
                id='node-search',
                type='text',
                placeholder='Enter node name...'
            ),
            html.Button('Highlight', id='highlight-button', n_clicks=0)
        ], style={'width': '20%', 'display': 'inline-block', 'padding': '20px'}),
        
        html.Div([
            cyto.Cytoscape(
                id='cytoscape',
                elements=elements,
                stylesheet=stylesheet,
                style={'width': '100%', 'height': '90vh'},
                layout={'name': 'dagre', 'animate': True},
                zoom=1,
                minZoom=0.1,
                maxZoom=2,
                boxSelectionEnabled=True,
                autolock=False,
                autoungrabify=False,
                autounselectify=False
            )
        ], style={'width': '75%', 'display': 'inline-block', 'height': '90vh'})
    ])

    # Add callbacks for interactivity
    @app.callback(
        Output('cytoscape', 'layout'),
        [Input('layout-dropdown', 'value'),
         Input('spacing-slider', 'value')]
    )
    def update_layout(layout_value, spacing):
        layout_config = {
            'name': layout_value,
            'animate': True,
            'animationDuration': 1000
        }
        
        # Add layout-specific parameters
        if layout_value == 'dagre':
            layout_config.update({
                'nodeDimensionsIncludeLabels': True,
                'spacingFactor': spacing/50
            })
        elif layout_value == 'cose-bilkent':
            layout_config.update({
                'idealEdgeLength': spacing,
                'nodeOverlap': 20,
                'refresh': 20
            })
        
        return layout_config

    @app.callback(
        Output('cytoscape', 'zoom'),
        Input('zoom-slider', 'value')
    )
    def update_zoom(zoom_value):
        return zoom_value

    @app.callback(
        Output('cytoscape', 'stylesheet'),
        Input('highlight-button', 'n_clicks'),
        [Input('node-search', 'value'),
         Input('cytoscape', 'tapNode')]
    )
    def highlight_node(n_clicks, search_term, tap_node):
        # Create a copy of the base stylesheet
        highlighted_stylesheet = stylesheet.copy()
        
        # Determine which node to highlight
        node_id = None
        if search_term:
            node_id = search_term
        elif tap_node:
            node_id = tap_node['data']['id']
        
        if node_id:
            highlighted_stylesheet.append({
                'selector': f'node[id = "{node_id}"]',
                'style': {
                    'background-color': '#FFD700',
                    'border-color': '#FF8C00',
                    'border-width': 3
                }
            })
            
            # Also highlight edges connected to this node
            highlighted_stylesheet.append({
                'selector': f'edge[source = "{node_id}"], edge[target = "{node_id}"]',
                'style': {
                    'line-color': '#FF8C00',
                    'target-arrow-color': '#FF8C00',
                    'width': 2
                }
            })
        
        return highlighted_stylesheet

    return app

if __name__ == '__main__':
    app = create_enhanced_dash_app("parent_child_data.xlsx")
    app.run(debug=True)
