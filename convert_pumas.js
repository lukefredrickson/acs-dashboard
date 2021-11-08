let mapshaper = require("mapshaper")

mapshaper.runCommands('-i data/pumas/shp/*.shp -o data/pumas/geojson/ format=geojson');