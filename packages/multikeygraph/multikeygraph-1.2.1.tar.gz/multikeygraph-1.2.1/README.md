# About

`multi-key-graph` is a command line tool that invokes `matplotlib` to
plot multiple keys on multiple graphs from an FSDB/pyfsdb data file
(tab-separated with a header).

# Installation

```
pip3 install multikeygraph
```

# Usage

`multi-key-graph` is designed to:

1. read in time-series data in FSDB format
2. Plot data in columns (-c COLNAME1 ...) for a given key column value (-k KEY).
3. Which key values to be plotted can be limited to a fixed list (-l VAL1 VAL2 ...)
4. Save the results to an output PNG file (-o OUT.png) or a window (-i)

If multiple columns are specified, the output will contain multiple
vertically stacked graphs with aligned X-axes allowing for easier
comparison of noisy time-series plots.

Plot labels can be specified using -T TITLE, --xlabel X-LABEL, and
--ylabel Y-LABEL.  By default line plots are drawn, unless a
dotted/scatter plot (-s) is requested.  Data should be pre-sorted for
line graphs.

A list of name=replacement values can be passed for legende name
replacements (-L name=replacement).  Anonymization of key values may
be specified with an anonymization pattern that includes a %d
specifier (-A "some%d").

# Published

* pypi: multikeygraph
* github: https://github.com/gawseed/multi-key-graph

# Author

Wes Hardaker @ USC/ISI

# See also

The FSDB website and manual page for the original perl module: 

https://www.isi.edu/~johnh/SOFTWARE/FSDB/
