# -*- coding: utf-8 -*-
"""
Created on Wed Dec  8 19:25:34 2021

@author: alexa

"""



def run_application():
    
    import pandas as pd
    import plotly.express as px
    import plotly.graph_objects as go
    
    import dash
    from dash import dcc, callback_context
    from dash import html
    from dash.dependencies import Input, Output
    
    import random
    import function_lib as fl




    
    app = dash.Dash(__name__)
    
    
#Alexander from line 32 to 106     
    df = pd.read_csv("overview/complete_tag_list.csv", encoding='utf-16', header=0) # loads the "complete_tag_list.py" file into a pandas data frames
    names= df.columns.str.split(',').tolist() # pull out the header to the names variable
    df= df.iloc[:,0].str.split(",", expand=True) # splits the one column df to three columns
    for element in names: # creates three strings in a list
        names=element
    df.columns = names # passes the names list to column names
    df['Counter'] = df['Counter'].astype(int) # changes the value type in the column 'Counter' to integer
    tags_count = df.groupby(df['Tag']).Counter.sum() # gives the sum of each tag per year
    
    
    
    app.layout = html.Div([
         html.Div([     
            
            
            # creates the dropdown for the tags
            dcc.Dropdown(
                id='dropdown',
                
                value=None,
                multi=True, 
                style={'width':"75%"},
                placeholder='Choose tag',
                className='form dropdown',
                ),
            
            
            
            
            #Creates a text area for multiline text
            dcc.Textarea(
            id='textarea-example',
            value='Choose the tags you want to see in the time based line chart.\nWant to see less tags? The slider adjusts the tag list as to occurrences per year',
            style={'width': '100%'},
            ),
            
            #Creates a slider
            dcc.Slider(
                id='tag_magnitude',
                min=1,
                max=40,
                step=1,
                value=1,
                marks={
                    0: {'label': '0 Tags'},
                    5: {'label': '5 Tags'},
                    10: {'label': '10 Tags'},
                    15: {'label': '15 Tags'},
                    20: {'label': '20 Tags'},
                    25: {'label': '25 Tags'},
                    30: {'label': '30 Tags'},
                    35: {'label': '35 Tags'},
                    40: {'label': '40 Tags'}
                    
                    }
                ),html.Div(id='slider_value1'),
            
            html.Div([dcc.Graph(id='bar_plot'),
            
            # dropdown to choose the amount of words in the word cloud
            dcc.Dropdown(
                id='Wordcloud_dropdown',
                options=[{'label': str(i)+" Words", 'value': i} for i in [10,50,100,200,500]],
                value=10,
                style={'width':'50%'}
                ),
            
            # textarea
            dcc.Textarea(
            id='wordcloud textarea',
            value='Word cloud of every article containing at least one of the tags above',
            style={'width': '50%'},
            ),
        html.Div([dcc.Graph(id='word-cloud'), 
     
#Chris from line 100 to 168                    
           dcc.Dropdown(
                id='dropdown_search',
                
                options=fl.get_search_term_dict(),
                value=None,
                multi=True, 
                style={'width':"75%"},
                placeholder='Choose word(s) to search for articles in the database',
                className='form dropdown',
                ),
       
                             
            dcc.Dropdown(
                id='dropdown_results',
                
                value=None, 
                style={'width':"75%"},
                placeholder='Found articles:',
                ),
     
    
            dcc.Textarea(
                id='show-selected-title',
                style={'width': '100%', 'height': 20}
                ),        
            dcc.Textarea(
                id='show-selected-article',
                style={'width': '100%', 'height': 800}
                ),
    
    
            dcc.Textarea(
                id='other-recommendations',
                value='Other articles you might like:',
                style={'width': '90%', 'height': 20}
                ),
            
            dcc.Textarea(
                id='recommended_article_1',
                style={'width': '18%', 'height': 40}
                ),
            dcc.Textarea(
                id='recommended_article_2',
                style={'width': '18%', 'height': 40}
                ),
            dcc.Textarea(
                id='recommended_article_3',
                style={'width': '18%', 'height': 40}
                ),
            dcc.Textarea(
                id='recommended_article_4',
                style={'width': '18%', 'height': 40}
                ),
            dcc.Textarea(
                id='recommended_article_5',
                style={'width': '18%', 'height': 40}
                ),
            
            html.Button('Open article',id='open_recommendation_1', n_clicks=0,style={'width':'18.25%'}),      
            html.Button('Open article',id='open_recommendation_2', n_clicks=0,style={'width':'18.25%'}), 
            html.Button('Open article',id='open_recommendation_3', n_clicks=0,style={'width':'18.25%'}), 
            html.Button('Open article',id='open_recommendation_4', n_clicks=0,style={'width':'18.25%'}), 
            html.Button('Open article',id='open_recommendation_5', n_clicks=0,style={'width':'18.25%'}), 
    
                            ]),
        ]), 
    ]),
         ])
    
    
    # takes the value from the slider as input
    # outputs to the dropdown menu.
    @app.callback( #Alexander
        Output('dropdown', 'options'),
        Input('tag_magnitude', 'value')
    )  
    # search the df for every tag with a 'Counter' larger than the slider value.
    def get_tag_list(slider_value): #Alexander
        tag_list = [{'label':tag.lower(), 'value':tag} for tag in df['Tag'].unique() if tags_count[tag] > slider_value]
        return tag_list
    
    
    # gets input from the first dropdown menu
    # output is the word cloud 
    @app.callback( #Alexander
        Output('bar_plot','figure'),
        Input('dropdown', 'value')
        )
    
    def tag_chart(dropdown_value): #Alexander
        # Puts all rows that contains the chosen tag(s) into the dff variable
        dff = df[df['Tag']==dropdown_value[0]]
        if len(dropdown_value) > 1:
            for i in range(1, len(dropdown_value)):
                tag = dropdown_value[i]
                temp_dff = df[df['Tag']==tag]
                dff = pd.concat([dff, temp_dff], axis=0)
        
        # Adds the year where the tags have not been used to a data frame,
        # and sets the 'Counter' to 0
        dummy_df = pd.DataFrame(columns=['Year', 'Tag', 'Counter'])
        for year in range(2014, 2022):
            for tag in dropdown_value:
                if ((dff['Year'] == str(year)) & (dff['Tag'] == tag)).any() == False:
                    temp_dff = {'Year': year, 'Tag': tag, 'Counter': 0}
                    dummy_df = dummy_df.append(temp_dff, ignore_index=True)
    
        # concatenates the to data frames, so every tag contains year 2014 to 2021        
        dff = pd.concat([dff, dummy_df], axis=0)
        dff['Year'] = dff['Year'].astype(str).astype(int)
        dff = dff.sort_values(by=['Tag', 'Year'])
    
        # Creates the line chart 
        fig = px.line(dff, x="Year", y="Counter", color="Tag")
        return fig
        
    
        # Gets input from the same dropdown as the line chart, and a 
        # dropdown that decides how many words to show in the cloud
        # Outputs the word cloud
    @app.callback( #Alexander
        Output('word-cloud','figure'),
        Input('Wordcloud_dropdown','value'),
        Input('dropdown', 'value'))
    def display_wordcloud(number, tag_list): #Alexander
        
        words = fl.find_article_words_from_tag(tag_list) # get a list containing two lists
        text = words[0] # takes the first list, which is the words 
        sizes = [int(min(60,max(i,10))) for i in words[1]] # takes the secon list, which is the size. Sets the min size to 10 and max size to 60.
    
        # Creates a scatterplot where each point is a word.    
        data = go.Scatter(x=random.choices(range(10*number), k=number),
                         y=random.choices(range(10*number), k=number),
                         mode='text',
                         text=text,
                         marker={'opacity': 0.8},
                         textfont={'size': sizes, 'color':'black'})
        layout = go.Layout({'xaxis': {'showgrid': False, 'showticklabels': False, 'zeroline': False},
                            'yaxis': {'showgrid': False, 'showticklabels': False, 'zeroline': False},
                            'height': 800})
        return go.Figure(data=[data], layout=layout)


# Feeds search terms to the search function and passes results back to user. 
# Returns a search instruction by default until a search has been made.      
    @app.callback( #Chris
        Output('dropdown_results', 'options'),
        Input('dropdown_search', 'value')
    )
    def get_found_articles(search_tag_list): #Chris
        if search_tag_list is None:
            return [{'label':'Search above first','value':'Search above first'}]
        return fl.return_searched_article_list(search_tag_list)
    
    
# Gets the article text, then passes it on along with a prettified titlename.       
    @app.callback( #Chris
        Output('show-selected-title', 'value'),
        Output('show-selected-article', 'value'),
        Input('dropdown_results', 'value')
    )
    def show_chosen_article(FILENAME): #Chris
        if FILENAME is None:
            return ''
        index = FILENAME.index('tag; ')
        return FILENAME[11:index], fl.open_requested_article(FILENAME)
    
    
# Splits the dictionary labels and values from the recommendation function into its relevant text areas and buttons.       
    @app.callback( #Chris
        Output('recommended_article_1','value'),
        Output('recommended_article_2','value'),
        Output('recommended_article_3','value'),
        Output('recommended_article_4','value'),
        Output('recommended_article_5','value'),
        Output('open_recommendation_1','value'),   
        Output('open_recommendation_2','value'), 
        Output('open_recommendation_3','value'), 
        Output('open_recommendation_4','value'), 
        Output('open_recommendation_5','value'), 
        Input('dropdown_results','value')
        )
    def get_recommendations(FILENAME): #Chris
        recommendation_table = fl.recommend_similar_articles(FILENAME)
        n1 = recommendation_table[0]['label']
        n2 = recommendation_table[1]['label']
        n3 = recommendation_table[2]['label']
        n4 = recommendation_table[3]['label']
        n5 = recommendation_table[4]['label']
        v1 = recommendation_table[0]['value']
        v2 = recommendation_table[1]['value']
        v3 = recommendation_table[2]['value']
        v4 = recommendation_table[3]['value']
        v5 = recommendation_table[4]['value']   
        return n1, n2, n3, n4, n5, v1, v2, v3, v4, v5
    
    
# Checks which button has most recently been clicked, then gives value of clicked button to to article reader.     
    @app.callback( #Chris
        Output('dropdown_results', 'value'),
        Input('open_recommendation_1', 'n_clicks'),
        Input('open_recommendation_1','value'),   
        Input('open_recommendation_2', 'n_clicks'),
        Input('open_recommendation_2','value'), 
        Input('open_recommendation_3', 'n_clicks'),
        Input('open_recommendation_3','value'), 
        Input('open_recommendation_4', 'n_clicks'),
        Input('open_recommendation_4','value'), 
        Input('open_recommendation_5', 'n_clicks'),
        Input('open_recommendation_5','value'),
        )
    def show_recommended_article(c1,v1,c2,v2,c3,v3,c4,v4,c5,v5): #Chris
        changed_id = [p['prop_id'] for p in callback_context.triggered][0]
        if 'open_recommendation_1.n_clicks' in changed_id:
            return v1
        if 'open_recommendation_2.n_clicks' in changed_id:
            return v2
        if 'open_recommendation_3.n_clicks' in changed_id:
            return v3
        if 'open_recommendation_4.n_clicks' in changed_id:
            return v4
        if 'open_recommendation_5.n_clicks' in changed_id:
            return v5
    
    app.run_server(debug=False)
    
