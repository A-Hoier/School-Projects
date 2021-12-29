# -*- coding: utf-8 -*-

with open("__init__.py", "w") as f:
    f.close()

#%%
import DS831lib as scraper

scraper.call_scrapes(2014,4,1) 

#%%
import backend_article_analysis_lib as analysis

analysis.create_json_tag_files()
analysis.make_complete_tag_list() 
analysis.analyze_articles()

#%%
import Dash_app

Dash_app.run_application()


