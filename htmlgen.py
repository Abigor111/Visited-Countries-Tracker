import folium
import geopandas as gpd
import pandas as pd

m = folium.Map(location=[0, 0], zoom_start=3,
    tiles="CartoDB Voyager")
# Carregar dados geográficos
world_countries_df = gpd.read_file("world_countries.shp")
world_countries_df.set_crs("EPSG:4326", inplace=True)
paises_visitados = ["Portugal", "Spain", "France", "Italy", "Netherlands", "Belgium", "Japan"]
paises_visitados_df = world_countries_df[world_countries_df["ADMIN"].isin(paises_visitados)]
paises_visitados_df["color"] = "green"
# Países por visitar
paises_por_visitar = ["Germany", "China", "United Kingdom"]
paises_por_visitar_df = world_countries_df[world_countries_df["ADMIN"].isin(paises_por_visitar)]
paises_por_visitar_df["color"] = "yellow"
# Merged Dataframe
paises_df = gpd.GeoDataFrame(pd.concat([paises_visitados_df, paises_por_visitar_df], ignore_index=True))
# Gerar mapa
tooltip = folium.GeoJsonTooltip(
    fields=["ADMIN"],
    aliases=["País:"],
    localize=True,
    sticky=False,
    labels=True,
    style="""
        background-color: #F0EFEF;
        border: 2px solid black;
        border-radius: 3px;
        box-shadow: 3px;
    """,
    max_width=500,
)


g = folium.GeoJson(
    paises_df,
    tooltip=tooltip,
        style_function=lambda feature: {
        "fillColor": feature["properties"]["color"],
        "color": "black",         # contorno
        "weight": 1,
        "fillOpacity": 0.6
    }
).add_to(m)
# Legenda
legend_html = '''
<div style="
    position: fixed;
    bottom: 50px;
    left: 50px;
    width: 150px;
    height: 90px;
    background-color: white;
    border:2px solid grey;
    z-index:9999;
    font-size:14px;
    padding: 10px;
    box-shadow: 3px 3px 6px rgba(0,0,0,0.3);
">
<b>Legenda</b><br>
<i style="background:green; width:18px; height:18px; float:left; margin-right:8px; opacity:0.7;"></i> País visitado<br>
<i style="background:yellow; width:18px; height:18px; float:left; margin-right:8px; opacity:0.7;"></i> País por visitar
</div>
'''
paises_visitados_len = len(paises_visitados)
paises_total = len(world_countries_df)
percentagem = (paises_visitados_len / paises_total) * 100
info_html = f'''
<div style="
    position: fixed;
    bottom: 20px;
    left: 50%;
    transform: translateX(-50%);
    background-color: white;
    border: 2px solid grey;
    z-index: 9999;
    font-size: 16px;
    font-weight: bold;
    padding: 12px 18px;
    border-radius: 8px;
    box-shadow: 3px 3px 6px rgba(0,0,0,0.3);
    text-align: center;
">
    Países visitados: {paises_visitados_len} / {paises_total}<br>
    ({percentagem:.1f}% do mundo)
</div>
'''

m.get_root().html.add_child(folium.Element(info_html))
m.get_root().html.add_child(folium.Element(legend_html))
m.save("mapa.html")