
# ### Dash

# In[54]:


#!pip install dash
#!pip install jupyter-dash
import datetime
import color_extract
from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
import base64

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H1("Extract Color"),
    dcc.Upload(
        id='upload-image',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        multiple=True
    ),
    html.Div(id='output-image-upload'),
])


@app.callback(Output('output-image-upload', 'children'),
              Input('upload-image', 'contents'),
              State('upload-image', 'filename'),
              State('upload-image', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):

    if list_of_contents is not None:
        output_name = color_extract.extract_color(list_of_names[0], 600, 12)
        encoded_image = base64.b64encode(open(output_name, 'rb').read())
        children = html.Div([
            html.H5(list_of_names[0]),
            html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()))
        ])
        return children

if __name__ == '__main__':
    app.run_server(debug=True)




