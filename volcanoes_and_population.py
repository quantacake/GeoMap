
import folium
import pandas as pd

# files
data = pd.read_csv('Volcanoes_USA.txt')

# variables
lat = data['LAT']
lon = data['LON']
name = data['NAME']
elev = data['ELEV']


# functions
def volc_color_maker(elevation):
    if elevation < 6000:
        return 'orange'
    elif elevation < 9000:
        return 'red'
    elif elevation < 12000:
        return 'green'
    else:
        return 'blue'

def pop_color_maker(population):
    if population < 1000000:
        return 'orange'
    elif population < 10000000:
        return 'red'
    elif population < 100000000:
        return 'darkred'
    else:
        return 'black'

def opacity_pop_adjustor(population):
    if population < 1000000:
        return 0.2
    elif population < 10000000:
        return 0.4
    elif population < 100000000:
        return 0.6
    else:
        return 0.8



# Layer 1 - map
map = folium.Map(
        location=[lat.median() ,lon.median()],
        zoom_start=5,
        tiles="Mapbox Bright"
        )


# Layer 2 - FeatureGroup (Volcanoes)
fg_volcanoes = folium.FeatureGroup(name='Volcanoes')

for la, lo, na, el in zip(lat, lon, name, elev):
    fg_volcanoes.add_child(folium.CircleMarker(
        location=[la, lo],
        radius=6,
        popup='{}: elev: {}'.format(na, str(int(round(el*3.28084)))),
        fill_color=volc_color_maker(round(el*3.28084))
        ))


# Layer 3 - FeatureGroup (World Population)
fg_population = folium.FeatureGroup(name='Population')

fg_population.add_child(folium.GeoJson(data=open('world.json', 'r', encoding='utf-8-sig').read(),
    style_function=lambda x: {'fillOpacity': opacity_pop_adjustor(x['properties']['POP2005']),
        'fillColor': 'blue'
        }))


# Add FeatureGroups to map layer (Base layer)
map.add_child(fg_volcanoes)
map.add_child(fg_population)

# Add Control Group to toggle layers on map
map.add_child(folium.LayerControl())


map.save('volcanoes_population.html')
