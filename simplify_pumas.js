let mapshaper = require("mapshaper")

mapshaper.runCommands('-i data/pumas/geojson/pumas.json -simplify keep-shapes percentage=0.15 -o force data/pumas/geojson/pumas.json');