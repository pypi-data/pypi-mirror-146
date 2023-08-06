Property Price Register
=======================

Easy way of interacting with property price register. Includes forward geocoding data so you can get cleaned addresses with latitude, longitude and the score of the match. I'm not paying for a forward geocoding service so as I use the free trial I'll update the data.

To enter a debugger with access to all sale data run `make load` (if working from the repo) or `load_property_price_register` if you have installed the package and you will have access to the variable `sales` which contains everything

Note that this data is fairly dirty, as more sources of data are brought in the data will become cleaner as time goes on. This is due to property price register having bad names and the forward geocoding not always being perfect.

Installation
------------

`pip install property-price-register`


Graphing
--------

```
usage: graph_property_price_register [-h] [--split-by SPLIT_BY] [--filter FILTER]

optional arguments:
  -h, --help           show this help message and exit
  --split-by SPLIT_BY  What to split by. Can be one of (blank (default), county, dublin_postal_code)
  --filter FILTER      When splitting by county or postal code or whateber, filter the selected fields by comma separated values like --filter="Dublin,Carlow,Mayo"
  --include-all        To include the total set of data as one label along with whatever other filters were used
  --remove-outliers    Remove sales with a price under 75k and a price of over 10m
```
