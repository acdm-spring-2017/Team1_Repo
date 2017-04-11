import sys
import numpy as np
from collections import OrderedDict

import bokeh.plotting as bk
from bokeh.layouts import layout
from bokeh.models.glyphs import Patches, Line, Circle
from bokeh.models import (GMapOptions,
    GMapPlot, DataRange1d, ColumnDataSource, LinearAxis,
    HoverTool, PanTool, WheelZoomTool, ResetTool, ZoomInTool, BoxSelectTool)
from bokeh.models import Toggle, CustomJS
from bokeh.resources import CDN
from bokeh.embed import components, autoload_static, autoload_server

from bokeh.io import output_file, show
from bokeh.resources import INLINE
from jinja2 import Template
from bokeh.util.browser import view

map_options = GMapOptions(lat=40.4420, lng=-79.9626, map_type = "roadmap", zoom=11)

plot = GMapPlot(
    x_range=DataRange1d(), y_range = DataRange1d(), map_options = map_options, plot_width = 1050 , plot_height=500
)

plot.title.text = "Pittsburgh"

plot.api_key="AIzaSyDlTxyDmCD2UfHzXabomEqETVxI_D2_Zu4"

plot.add_tools(PanTool(), WheelZoomTool(), ZoomInTool(),
	    ResetTool(), BoxSelectTool())

with open('group_tracker_complete.csv') as f:
    myfile = f.read()
import pandas as pd
df = pd.read_csv('group_tracker_complete.csv')

source = ColumnDataSource(
    data=dict(
        jiayin_lats = list(df['lat'][1:79]),
        jiayin_longs = list(df['lon'][1:79]),
        jahari_lats=list(df['lat'][80:220]),
        jahari_longs=list(df['lon'][80:220]),
        connor_lats=list(df['lat'][221:3466]),
        connor_longs=list(df['lon'][221:3466]),
        kat_lats=list(df['lat'][3467:3831]),
        kat_longs=list(df['lon'][3467:3831]),
        maya_lats=list(df['lat'][3831:]),
        maya_longs=list(df['lon'][3831:])
    )
)
circle1 = Circle(x='jiayin_longs', y='jiayin_lats', size=5, fill_color="#9ABF2D", fill_alpha=0.8, line_color=None)
circle2 = Circle(x='jahari_longs',y='jahari_lats', size=5, fill_color="#EBB523", fill_alpha=0.8, line_color=None)
circle3 = Circle(x='connor_longs',y='connor_lats', size=5, fill_color="#D13863", fill_alpha=0.8, line_color=None)
circle4 = Circle(x='kat_longs',y='kat_lats', size=5, fill_color="#42A4BF", fill_alpha=0.8, line_color=None)
circle5 = Circle(x='maya_longs',y='maya_lats', size=5, fill_color="#AE3FD3", fill_alpha=0.8, line_color=None)

# We write coffeescript to link toggle with visible property of box and line
code = '''\
object.visible = toggle.active
'''
#jaiyin=p.add_glyph(source, circle1)
#jahari=p.add_glyph(source,circle2)
#connor=p.add_glyph(source,circle3)
#kat=p.add_glyph(source,circle4)
#maya=p.add_glyph(source,circle5)
#everyone=[p.add_glyph(source,circle1),p.add_glyph(source,circle2),p.add_glyph(source,circle3),
#p.add_glyph(source,circle4),p.add_glyph(source,circle5)]

callback1 = CustomJS.from_coffeescript(code=code, args={})
toggle1 = Toggle(label="Jiayin", button_type="success", callback=callback1, width=200)
callback1.args = {'toggle': toggle1, 'object':plot.add_glyph(source, circle1) }

callback2 = CustomJS.from_coffeescript(code=code, args={})
toggle2 = Toggle(label="Jahari", button_type="success", callback=callback2, width=200)
callback2.args = {'toggle': toggle2, 'object':plot.add_glyph(source,circle2)}

callback3 = CustomJS.from_coffeescript(code=code, args={})
toggle3 = Toggle(label="Connor", button_type="success", callback=callback3, width=200)
callback3.args = {'toggle': toggle3, 'object':plot.add_glyph(source,circle3)}

callback4 = CustomJS.from_coffeescript(code=code, args={})
toggle4 = Toggle(label="Kat", button_type="success", callback=callback4, width=200)
callback4.args = {'toggle': toggle4, 'object':plot.add_glyph(source,circle4)}

callback5 = CustomJS.from_coffeescript(code=code, args={})
toggle5 = Toggle(label="Maya", button_type="success", callback=callback5, width=200)
callback5.args = {'toggle': toggle5, 'object':plot.add_glyph(source,circle5)}

script, div = components(plot)
js_resources = INLINE.render_js()
css_resources = INLINE.render_css()

template = Template('''<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <title>Widget</title>
        {{ js_resources }}
        {{ css_resources }}
    </head>
    <body>
        {{ div }}
        {{ script }}
    </body>
</html>
''')

filename = "plot.html"

html = template.render(js_resources=js_resources,
        css_resources=css_resources,
        script=script,
        div=div)
with open(filename, 'w') as f:
    f.write(html)

view(filename)

bk.output_file("Team1.html")

bk.show(layout([plot],[toggle1,toggle2,toggle3,toggle4,toggle5]))
