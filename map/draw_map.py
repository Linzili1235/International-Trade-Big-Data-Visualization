#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 10 01:44:28 2022

@author: jiahuiwu
"""
from boundary import boundary_dict 
import folium
import geopandas as gpd
from folium import plugins
from shapely.geometry import Polygon
from descartes import PolygonPatch



USA = gpd.read_file("/Users/jiahuiwu/Downloads/geoBoundaries-USA-ADM0-all/geoBoundaries-USA-ADM0.geojson")

def generateBasemap():
    map1 = folium.Map(location=[40.7, -73.98], zoom_start = 2)
    
    for k,r in boundary_dict.items():
        if r!= 'error':
            for poly in r:
                poly = Polygon(poly[0])
                sim_geo = gpd.GeoSeries(poly).simplify(tolerance=0.0001)
                geo_j = sim_geo.to_json()
                geo_j = folium.GeoJson(data=geo_j,
                                   style_function=lambda x: {'fillColor': 'yellow','color':'black','weight':1})
                folium.Popup(k).add_to(geo_j)
            
            geo_j.add_to(map1)
    #USA
    allparts = [p.buffer(0) for p in USA["geometry"][0]]
    for r in allparts:
        sim_geo = gpd.GeoSeries(r).simplify(tolerance=0.0001)
        geo_j = sim_geo.to_json()
        geo_j = folium.GeoJson(data=geo_j,
                           style_function=lambda x: {'fillColor': 'pink','color':'black','weight':1.5})
        folium.Popup("United States").add_to(geo_j)
        geo_j.add_to(map1)
    
    return(map1)


basemap = generateBasemap()
basemap.save("basemap.html")



#############________________________________
#add data

from dataClean import data, filenames
import datetime




#generate feature

def type_color(Type):
    if Type =='import':
       return  "red"
    else:
        return "blue"

def generate_feature(filename):
    Type = filename.split('_')[2]
    
    features = [
        {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": point["coordinates"] ,
            },
            "properties": {
                "time": str(point["datetime"]),
                'style': {'color' : ''},
                    'icon': 'circle',
                    'iconstyle':{
                        'fillColor': type_color(Type),
                        'fillOpacity': 0.8,
                        'stroke': 'true',
                        'radius': point['sum_value']/1000000000 
                    }
            },
        }  for point in data[filename]
       
    ]
    
    return features
    

def draw_point():
    points_import = []
    points_export = []
    for name in filenames:
        Type = name.split('_')[2]
        if(Type) == "import":
            points_import.extend(generate_feature(name))
        else:
            points_export.extend(generate_feature(name))
    
    map1 = generateBasemap()
    map2 = generateBasemap()
    
    plugins.TimestampedGeoJson(points_import,
                         period = 'PT1Y',
                         duration = 'PT1Y',
                         transition_time = 200,
                         auto_play = True).add_to(map1)
    
    plugins.TimestampedGeoJson(points_export,
                         period = 'PT1Y',
                         duration = 'PT1Y',
                         transition_time = 200,
                         auto_play = True).add_to(map2)
    map1.save('import.html')
    map2.save('export.html')

    
    
        
        
    
