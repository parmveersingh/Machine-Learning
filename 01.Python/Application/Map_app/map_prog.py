import folium
maps = folium.Map(location=[30.4,75.3],tiles='Mapbox Bright')
maps.add_child(folium.CircleMarker(location=[30.4,75.3],popup="Punjab"))
maps.add_child(folium.Html("<b>ii how are you!</b>",True,"100%","20%"))
maps.save("map1.html")
