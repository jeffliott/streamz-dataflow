from streamz import Stream
import json
import csv

def preprocess_stream(preprocs, stream):
    for prep in preprocs:
        func = prep["func"]
        params = {}
        if "parameters" in prep:
            params = prep["parameters"]
        if func == "lower":
            stream = stream.map(str.lower)
    return stream

def parse_mock_json_source(source):
    data = json.loads(source["parameters"]["raw"])
    return [data for x in range(0, source["parameters"]["repeat"])], Stream()    

def parse_mock_csv_source(source):
    params = source["parameters"]
    preproc = source["preprocess"]
    data = csv.DictReader(params["raw"], fieldnames=params["fields"])
    stream = preprocess_stream(preproc, Stream())
    return data, stream

def parse_json_source(source):
    params = source["parameters"]
    return open(params["filename"], "r"), Stream()

def parse_sources(sources):
    TYPE_MAP = {
        "MockJsonSource" : parse_mock_json_source,
        "MockCsvSource" : parse_mock_csv_source,
        "JsonSource" : parse_json_source,
    }
    streams = []
    for source in sources:
        stream = TYPE_MAP[source["type"]](source)
        streams.append(stream)
    return streams

def norm_to_ecs(row, params):
    return row

def lookup_geo_from_ip(row, params):
    return row

def tag(row, params):
    return row

def parse_dataflow(df):
    so = Stream()
    s = so
    for flow in df:
        func = flow["func"]
        params = {}
        if "parameters" in flow:
            params = flow["parameters"]
        if func == "norm_to_ecs":
            s = s.map(norm_to_ecs, params)
        if func == "lookup_geo_from_ip":
            s = s.map(lookup_geo_from_ip, params)
        if func == "tag":
            s = s.map(tag, params)
    return so, s

def parse_debug_console(df, params):
    return df.sink(print)

def parse_file_direct(df, params):
    return df.sink_to_textfile(params["filename"])

def parse_sinks(sinks, stream):
    SINK_MAP = {
        "DebugConsole" : parse_debug_console,
        "FileDirect" : parse_file_direct
    }
    streams = []
    for sink in sinks:
        stream = SINK_MAP[sink["type"]](stream, sink["parameters"])
        streams.append(stream)
    return streams
        

with open("dataflows/example.json") as fd:
    dataflow = json.load(fd)
    sources = parse_sources(dataflow["sources"])
    ds, df = parse_dataflow(dataflow["dataflow"])
    for d, s in sources:
        s.connect(ds)
    sinks = parse_sinks(dataflow["sinks"], df)
    for sink in sinks:
        df.connect(sink)
    df.visualize("df.png")
    for d, s in sources:
        for r in d:
            s.emit(str(r))

