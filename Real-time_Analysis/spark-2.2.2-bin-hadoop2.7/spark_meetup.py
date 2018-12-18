import json
import sys

from pyspark import SparkContext, SparkConf
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

import holoviews as hv

from holoviews.streams import Pipe, Buffer

import streamz
import streamz.dataframe

from bokeh.plotting import figure
from bokeh.models import ColumnDataSource

hv.extension('bokeh')

def country_count_update(newValue, existingCount):
    if existingCount is None:
        existingCount = 0
    
    return sum(newValue)+existingCount

def send_to_bokeh(country_count_dict):
    output_file("meetup_country_count.html")

    source = ColumnDataSource(data=dict(countries=[], counts=[], color=Spectral6))
    source.stream(country_count_dict)
    p = figure(x_range = sorted_countires, plot_height=250, title="Meetup country count", toolbar_location=None, tools="")
    p.vbar(x=countries, top=counts, width=0.9, color='color', source=source)

    p.xgrid.grid_line_color=None
    p.y_range.start=0

if __name__ == '__main__':
    conf = SparkConf().setMaster("local[2]").setAppName("MeetupRsvpAnalytics").set("spark.ui.port", "44040")
    sc = SparkContext(conf=conf)
    sc.setLogLevel("ERROR")
    ssc = StreamingContext(sc, 2)
    ssc.checkpoint("checkpoint")
    
    broker, topic = sys.argv[1:]
    kvs = KafkaUtils.createStream(ssc, broker, "raw-event-streaming-consumer", {topic: 1})
    rsvps_json = kvs.map(lambda x: json.loads(x[1].encode('ascii','ignore')))
    rsvps_city_pair = rsvps_json.map(lambda x: (x['group']['group_country'],1))
    rsvps_city_statefulCount = rsvps_city_pair.updateStateByKey(country_count_update)

    for y in rsvps_city_statefulCount:
        send_to_bokeh(y)

    send_to_bokeh(rsvps_city_statefulCount)
    ssc.start()
    ssc.awaitTermination()
    ssc.stop()