import folium 
import gpxpy
import os
import base64
from PIL import Image
import PIL
import folium.plugins as plugins		# tylko tak działają pluginsy
from branca.element import Template, MacroElement
from image_edition import image_edition
from image_edition import image_edition_1
from image_edition import image_edition_2
# https://towardsdatascience.com/how-to-deploy-your-data-science-as-web-apps-easily-with-python-955dd462a9b5


def overlayGPX(gpxDataList, Colours, Labels, zoom):
	myMap = folium.Map(location=[50.443627, 16.869285],zoom_start=zoom)
	# add the layer control
	LC = folium.map.LayerControl(position='topleft', collapsed=True, autoZIndex=True)

	# deklaracja warstw
	L1 = folium.FeatureGroup()
	L2 = folium.FeatureGroup()
	L3 = folium.FeatureGroup()
	L4 = folium.FeatureGroup()
	L5 = folium.FeatureGroup()
	L6 = folium.FeatureGroup()
	L7 = folium.FeatureGroup()
	
	# tyt warstwy
	L1.layer_name = 'Szlaki komunikacyjne'
	L2.layer_name = 'Niekóre atrakcje obecne w roku 2020'
	L3.layer_name = 'Ważna działka w centrum miasta'
	L4.layer_name = 'Proponowany podział ważnej działki w centrum miasta'
	L5.layer_name = 'Propozycje uczestników SLL'
	L6.layer_name = 'Nowe atrakcje'
	L7.layer_name = 'Przegląd ankietyzacji kolarzy górskich'

	# dodawanie tytułu
	title_html = '''
			 <h3 align="center" style="font-size:17px"><b>Gmina Złoty Stok - przestrzenne rozmieszczenie elementów raportu</b></h3>
			 '''
	myMap.get_root().html.add_child(folium.Element(title_html))

	# dodawanie szlakow z plików GPX
	for gpxData, color, label in zip(gpxDataList, Colours, Labels):
		gpx_file = open(gpxData, 'r')
		Lon = []
		Lat = []
		for line in gpx_file:
			X = line.split('"')
			
			for i in X:
				try:
					if float(i) < 20:
						Lon.append(float(i))
					elif float(i) > 20:
						Lat.append(float(i))
				except:
					pass
		points = [];
		for i, j in zip(Lat[2:], Lon[2:]):
			points.append([i, j])
		if gpxData == 'zloty-stok-czerwona.gpx' or gpxData == 'zloty-stok-niebieska.gpx':
			(folium.vector_layers.PolyLine(points, width = '200%', popup=label, tooltip=None, smooth_factor = 2, color=color, dash_array='5')).add_to(L1)
		else:
			(folium.vector_layers.PolyLine(points, width = '200%', popup=label, tooltip=None, smooth_factor = 2, color=color)).add_to(L1)

	################################################################
	################################################################
	# OBRAZY ISTNIEJACYCH ATRAKCJI
	################################################################
	# singletracki
	png = "single.png"
	encoded = base64.b64encode(open(png, 'rb').read())
	html = '''<h3>Sieć szlaków rowerowych Singletrack Glacensis</h3>
	<br><img src="data:image/png;base64,{}">
	<br><p></p>'''.format
	iframe = folium.IFrame(html(encoded.decode('UTF-8')), width=420, height=420)
	popup = folium.Popup(iframe, max_width=500)
	icon = folium.Icon(color="red", icon="ok")
	marker = folium.Marker(location=[50.441834, 16.865620], popup=popup, icon=icon)
	marker.add_to(L2)

	# wypożyczalnia rowerów elektrycznych
	png = 'ebike.png'
	encoded = base64.b64encode(open(png, 'rb').read())
	html = '''<h3>Wypożyczalnia rowerów elektrycznych <em>Segbi</em></h3>
	<br><img src="data:image/png;base64,{}">
	<br><p></p>'''.format
	iframe = folium.IFrame(html(encoded.decode('UTF-8')), width=430, height=340)
	popup = folium.Popup(iframe, max_width=500)
	icon = folium.Icon(color="red", icon="ok")
	marker = folium.Marker(location=[50.442673, 16.875021], popup=popup, icon=icon)
	marker.add_to(L2)

	# kaplica cmentarna
	png = 'cmentarz_2.png'
	encoded = base64.b64encode(open(png, 'rb').read())
	html = '''<h3>Późnogotycka Kaplica Cmentarna</h3>
	<br><img src="data:image/png;base64,{}">
	<br><p></p>'''.format
	iframe = folium.IFrame(html(encoded.decode('UTF-8')), width=310, height=520)
	popup = folium.Popup(iframe, max_width=310)
	icon = folium.Icon(color="red", icon="ok")
	marker = folium.Marker(location=[50.445561, 16.875297], popup=popup, icon=icon)
	marker.add_to(L2)

	# kamienica na rynku z portretami
	png = 'zloty1_kamienica_z_portretami.png'
	encoded = base64.b64encode(open(png, 'rb').read())
	html = '''<h3><em>Rynek</em> i jedna z wielu<br/>zabytkowych kamienic</h3>
	<br><img src="data:image/png;base64,{}">
	<br><p></p>'''.format
	iframe = folium.IFrame(html(encoded.decode('UTF-8')), width=420, height=420)
	popup = folium.Popup(iframe, max_width=420)
	icon = folium.Icon(color="red", icon="fa-university", prefix = 'fa')
	marker = folium.Marker(location=[50.442969, 16.874835], popup=popup, icon=icon)
	marker.add_to(L2)

	# 'wyrobisko'/skala za kopalnią
	png = 'skala.png'
	encoded = base64.b64encode(open(png, 'rb').read())
	html = '''<h3>Widok na potężne wyrobisko i tyrolkę</h3>
	<br><img src="data:image/png;base64,{}">
	<br><p></p>'''.format
	iframe = folium.IFrame(html(encoded.decode('UTF-8')), width=420, height=400)
	popup = folium.Popup(iframe, max_width=420)
	icon = folium.Icon(color="red", icon="ok")
	marker = folium.Marker(location=[50.436968, 16.872321], popup=popup, icon=icon)
	marker.add_to(L2)

	# meleks zdjecie z gazety
	png = 'melex.png'
	encoded = base64.b64encode(open(png, 'rb').read())
	html = '''<h3>Punkt Informacji Turystycznej i możliwość zwiedzania miasta melexem</h3>
	<br><img src="data:image/png;base64,{}">
	<br><p></p>'''.format
	iframe = folium.IFrame(html(encoded.decode('UTF-8')), width=420, height=400)
	popup = folium.Popup(iframe, max_width=420)
	icon = folium.Icon(color="red", icon="ok")
	marker = folium.Marker(location=[50.442837, 16.874020], popup=popup, icon=icon)
	marker.add_to(L2)

	# park techniki
	png = 'park_techniki_2.png'
	encoded = base64.b64encode(open(png, 'rb').read())
	html = '''<h3>Średniowieczny Park Techniki</h3>
	<br><img src="data:image/png;base64,{}">
	<br><p></p>'''.format
	iframe = folium.IFrame(html(encoded.decode('UTF-8')), width=420, height=460)
	popup = folium.Popup(iframe, max_width=420)
	icon = folium.Icon(color="red", icon="ok")
	marker = folium.Marker(location=[50.444541, 16.879349], popup=popup, icon=icon)
	marker.add_to(L2)

	################################################################
	################################################################
	# NASZE POMYSŁY
	################################################################

	# wiata gastronomiczna na rynku lub obok singla
	png = 'wiata.png'
	encoded = base64.b64encode(open(png, 'rb').read())
	html = '''<h3>Przykładowe wykonanie i poglądowe umiejscowienie wiaty gastronomicznej</h3>
	<br><img src="data:image/png;base64,{}">
	<br><p></p>'''.format
	iframe = folium.IFrame(html(encoded.decode('UTF-8')), width=420, height=400)
	popup = folium.Popup(iframe, max_width=420)
	icon = folium.Icon(color="green", icon="home")
	marker = folium.Marker(location=[50.440978, 16.874471], popup=popup, icon=icon)
	marker.add_to(L5)

	# napisy promocyjne z hashtagiem przy wjazdach do miasta
	png = 'zdjecie_napisu.png'
	encoded = base64.b64encode(open(png, 'rb').read())
	html = '''<h3>Napisy powiązane z akcją promocyjną</h3>
	<br><img src="data:image/png;base64,{}">
	<br><p></p>'''.format
	iframe = folium.IFrame(html(encoded.decode('UTF-8')), width=410, height=400)
	popup = folium.Popup(iframe, max_width=420)
	icon = folium.Icon(color="green", icon="fa-hashtag", prefix = 'fa')
	marker = folium.Marker(location=[50.447121, 16.864869], popup=popup, icon=icon)
	marker.add_to(L5)

	# atrakcyjne dzialki
	png = 'pole.png'
	encoded = base64.b64encode(open(png, 'rb').read())
	html = '''<h3>Korzystny dla miasta podział działki</h3>
	<br><img src="data:image/png;base64,{}">
	<br><p></p>'''.format
	iframe = folium.IFrame(html(encoded.decode('UTF-8')), width=420, height=485)
	popup = folium.Popup(iframe, max_width = 420)
	icon = folium.Icon(color = "green", icon = "fa-pie-chart", prefix = 'fa')
	marker = folium.Marker(location=[50.445954, 16.873068], popup=popup, icon=icon)
	marker.add_to(L5)


	###############################################################
	# PODZIAŁ DZIAŁEK
	###############################################################

	# Wyznaczanie (pogladowe) dzialki
	oryginal_field = folium.vector_layers.Polygon([[50.446811, 16.873717], [50.445823, 16.873545], [50.445416, 16.873196], [50.445481, 16.873051]], popup="Działka w aktualnej postaci", fill_color='blue')
	biedronka_field = folium.vector_layers.Polygon([[50.445922, 16.871966], [50.446862, 16.873631], [50.446811, 16.873717], [50.446227, 16.873619], [50.445643, 16.872632]], popup="Działka supermarketu po zamianie", fill_color='green')
	golden_field = folium.vector_layers.Polygon([[50.445823, 16.873545], [50.445416, 16.873196], [50.445643, 16.872637], [50.446215, 16.873622]], popup = "Działka miasta po zamianie", fill_color = 'red')
	oryginal_field.add_to(L3)
	biedronka_field.add_to(L4)
	golden_field.add_to(L4)
	
	################################################################
	################################################################


	################################################################
	################################################################
	# POWSTAJACE ATRAKCJE
	################################################################

	# sciezka laczaca kopalnie z rynkiem
	png = 'trasa.png'
	encoded = base64.b64encode(open(png, 'rb').read())
	html = '''<h3>Atrakcyjna ścieżka kopalnia-rynek</h3>
	<br><img src="data:image/png;base64,{}">
	<br><p></p>'''.format
	iframe = folium.IFrame(html(encoded.decode('UTF-8')), width=420, height=400)
	popup = folium.Popup(iframe, max_width = 420)
	icon = folium.Icon(color = "darkgreen", icon = "fa-child", prefix = 'fa')
	marker = folium.Marker(location=[50.440397, 16.875159], popup=popup, icon=icon)
	marker.add_to(L6)

	# wieża widokowa na kościele ewangelickim
	png = "wieza.png"
	encoded = base64.b64encode(open(png, 'rb').read())
	html = '''<h3>Platforma widokowa na szczycie wieży kościelnej</h3>
	<br><img src="data:image/png;base64,{}">
	<br><p></p>'''.format
	iframe = folium.IFrame(html(encoded.decode('UTF-8')), width = 320, height=520)
	popup = folium.Popup(iframe, max_width = 320)
	icon = folium.Icon(color = "darkgreen", icon = "fa-child", prefix = 'fa')
	marker = folium.Marker(location=[50.442686, 16.873486], popup=popup, icon=icon)
	marker.add_to(L6)

	################################################################
	################################################################
	# ANALIZA ANKIETY
	################################################################

	# wieża widokowa na kościele ewangelickim
	png = image_edition_1("pie_chart")
	encoded = base64.b64encode(open(png, 'rb').read())
	html = '''<br><img src="data:image/png;base64,{}">
	<br><p></p>'''.format
	iframe = folium.IFrame(html(encoded.decode('UTF-8')), width = 820, height=620)
	popup = folium.Popup(iframe, max_width = 820)
	icon = folium.Icon(color = "cadetblue", icon = "fa-line-chart", prefix = 'fa')
	marker = folium.Marker(location=[50.435845, 16.861167], popup=popup, icon=icon)
	marker.add_to(L7)

	# dodawanie warstw do mapy
	L1.add_to(myMap)
	L2.add_to(myMap)
	L3.add_to(myMap)
	L4.add_to(myMap)
	L5.add_to(myMap)
	L6.add_to(myMap)
	L7.add_to(myMap)
	LC.add_to(myMap)

	
	template = """
	{% macro html(this, kwargs) %}

	<!doctype html>
	<html lang="en">
	<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<title>jQuery UI Draggable - Default functionality</title>
	<link rel="stylesheet" href="//code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css">

	<script src="https://code.jquery.com/jquery-1.12.4.js"></script>
	<script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>

	<script>
	$( function() {
	$( "#maplegend" ).draggable({
					start: function (event, ui) {
						$(this).css({
							right: "auto",
							top: "auto",
							bottom: "auto"
						});
					}
				});
	});

	</script>
	</head>
	<body>


	<div id='maplegend' class='maplegend' 
	style='position: absolute; z-index:9999; border:2px solid grey; background-color:rgba(255, 255, 255, 0.8);
	 border-radius:6px; padding: 10px; font-size:14px; right: 20px; bottom: 20px;'>
	 
	<div class='legend-title'>Legenda znaczników</div>
	<div class='legend-scale'>
	<ul class='legend-labels'>
	<li><span style='background:#d33d29;opacity:1;'></span>Atrakcje obecne w roku 2020</li>
	<li><span style='background:#6da824;opacity:1;'></span>Propozycje uczestników SLL</li>
	<li><span style='background:#6f7f23;opacity:1;'></span>Powstające atrakcje</li>
	<li><span style='background:#FF5050;opacity:1;'></span>Ścieżka prowadząca od kopalni do rynku</li>
	<li><span style='background:#349ceb;opacity:1;'></span>(i inne odcienie niebieskiego) Ważne szlaki komunikacyjne</li>
	<li><span style='background:#5f9ea0;opacity:1;'></span>Wyniki ankietyzacji kolarzy</li>

	</ul>
	</div>
	</div>

	</body>
	</html>

	<style type='text/css'>
	.maplegend .legend-title {
	text-align: left;
	margin-bottom: 5px;
	font-weight: bold;
	font-size: 80%;
	}
	.maplegend .legend-scale ul {
	margin: 0;
	margin-bottom: 5px;
	padding: 0;
	float: left;
	list-style: none;
	}
	.maplegend .legend-scale ul li {
	font-size: 70%;
	list-style: none;
	margin-left: 0;
	line-height: 18px;
	margin-bottom: 2px;
	}
	.maplegend ul.legend-labels li span {
	display: block;
	float: left;
	height: 16px;
	width: 30px;
	margin-right: 5px;
	margin-left: 0;
	border: 1px solid #999;
	}
	.maplegend .legend-source {
	font-size: 70%;
	color: #777;
	clear: both;
	}
	.maplegend a {
	color: #777;
	}
	</style>
	{% endmacro %}"""

	macro = MacroElement()
	macro._template = Template(template)

	myMap.get_root().add_child(macro)

	folium.plugins.Fullscreen(
	position='topright',
	title='wypełnij ekran',
	title_cancel='wyłącz tryb pełnego ekranu',
	force_separate_button=True).add_to(myMap)
	return(myMap)

overlayGPX(['klodzko_valid.gpx', 'kopalnia.gpx', 
	'bila_woda.gpx', 'zloty-stok-czerwona.gpx', 
	'zloty-stok-niebieska.gpx'], ['#349ceb', '#FF5050', 
	'#3459eb', '#038cfc', '#038cfc'], 
	['Trasa łącząca Złoty Stok z Kłodzkiem', 
	'Ścieżka między rynkiem a kopalnią', 
	'Trasa łącząca Złoty Stok z Białą Wodą', 
	'Trasa Single Track Glacensis Złoty Stok Czerwona', 
	'Trasa Single Track Glacensis Złoty Stok Niebieska'], 15).save("SLL_map.html")

# dodaj zielony znacznik do pól
# WAZNE w przyszlosci aby miec pole do popisu z kolorami markerow
# mozna uzyc class folium.plugins.BeautifyIcon
# <li><span style='background:#349ceb;opacity:1;'><span style='background:#3459eb;opacity:1;'><span style='background:#34ebe5;opacity:1;'><span style='background:#34ebe5;opacity:1;'></span><span style='background:#FF5050;opacity:1;'></span>Atrakcje obecne w roku 2020</li>
