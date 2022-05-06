#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  5 22:54:18 2022

@author: jiahuiwu
"""

from boundary import boundary_dict 
import folium
import geopandas as gpd
from shapely.geometry import Polygon

import pandas as pd
from dataClean import data, filenames


from folium.plugins import TimeSliderChoropleth



USA = gpd.read_file("geoBoundaries-USA-ADM0.geojson")

def Basemap():
    map1 = folium.Map(zoom_start = 2.5,location=[40.7, -43.98], tiles='cartodbpositron',max_bounds=True, max_zoom = 3, min_zoom = 2.5)
    return(map1)


basemap = Basemap()
basemap.save("basemap.html")

import branca.colormap as cm

def generate_df(Type):
    geometry_df = pd.DataFrame()
    geo_list = []
    value_list = []   
    time_list = []
    country_list = []
    for filename in filenames:
        if filename.split('_')[2] == Type:
            for point in data[filename]:
                geo = boundary_dict[point['country']];
                if(geo != 'error'):
                    for poly in geo:
                        len_limit = sorted([len(poly[0]) for poly in geo], reverse = True)[0]
                        if(len(poly[0]) >= len_limit):
                            poly = Polygon(poly[0]).simplify(0.1)
                            geo_list.append(poly)
                            value_list.append(int(point['sum_value'] / 10**9))
                            time_list.append(point["datetime"])
                            country_list.append(point["country"])
                    
                
    geometry_df['geometry'] = geo_list
    geometry_df['time'] = time_list
    geometry_df['value'] = value_list
    geometry_df['country'] = country_list
    
    return geometry_df



import_df = generate_df("import")
export_df = generate_df("export")




def drawMap(df):
    df['date_sec'] = pd.to_datetime(df['time']).astype(int) / 10**9 


    df['date_sec'] = df['date_sec'].astype(int) + 100000


    max_colour = max(df['value'])
    min_colour = min(df['value'])
    cmap = cm.step.YlOrRd_09.to_linear().scale(min_colour, max_colour)
    df['color'] = df['value'].map(cmap)



    countries_gdf = gpd.GeoDataFrame(df['geometry'])['geometry'].simplify(0.1)
    # countries_gdf = countries_gdf.drop_duplicates().reset_index()            


    country_list = df['country'].tolist()
    country_idx = range(len(country_list))

    style_dict = {}
    for i in country_idx:
        country = country_list[i]
        result = df[df['country'] == country]
        inner_dict = {}
        for _, r in result.iterrows():
            inner_dict[r['date_sec']] = {'color': r['color'], 'opacity': 0.7}
        style_dict[i] = inner_dict



    map1 = Basemap()
    _ = TimeSliderChoropleth(
        data=countries_gdf.to_json(),
        styledict=style_dict).add_to(map1)

    _ = cmap.add_to(map1)
    cmap.caption = "sum of trade value (in trillion)"
    

    return map1
        

drawMap(import_df).save('import.html')
drawMap(import_df).save('export.html')
        












