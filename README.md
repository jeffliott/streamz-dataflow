# streamz-dataflow

## dataflows/example.json:
    a rudimentary dataflow specification.
## dataflows/test_data.json:
    some seriously stupid test data.
## src/python/streamz-dataflow.py:
    parses the example.json file and builds a streamz dataflow based on its contents.
    Its really bad.
    After writing this, I'm kind of wondering why noone has done this already for streamz.

# Goals
1) Might actually invest in this and make a generic dataflow parser for streamz to let arbitrary dataflows be specified in a configuration file without the need to write a lot of code.
2) Duplicate some of benthos's features without really inventing things like bloblang.
3) Have fun. Feel like a proper engineer for a bit.
4) Seriously wonder why anyone on earth would bother to write their own pipeline software when it is hard enough to make a good dataflow itself.
5) Kill some time and do something open source.