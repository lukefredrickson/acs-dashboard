# American Community Survey Dashboard
### Author: Luke Fredrickson
### Last Updated: 10/11/2021

## Quick Start Guide
### Git setup

Install [git](https://git-scm.com/) if you don't have it, then clone this repository into a new folder:

```shell
git clone https://github.com/lukefredrickson/acs-dashboard.git
cd acs-dashboard
```
### Python setup

Install the required Python packages by running the following command. Creating a new Python virtual environment first is recommended (for further instructions see the [official Python documentation](https://docs.python.org/3/tutorial/venv.html) for virtual environments).

```shell
python -m pip install -r requirements.txt
```

### NodeJS setup

The [mapshaper](https://github.com/mbloch/mapshaper#readme) javascript package is required to run this program. This requires NodeJS to be installed locally on your machine. Follow the steps [here](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm) to install NodeJS and npm. Once Node is installed, run

```shell
npm i
```

to install mapshaper locally.

### Data setup

Use the provided scripts to automatically download and modify the ACS PUMS and PUMAs data. These may take a while to run, depending on your internet speed. For a verbose explanation, see the [Downloading and Setting up Data Files](#downloading-and-setting-up-data-files) section.

The following scripts download the PUMA shapefiles, convert them to GEOJSON format, consolidate them into one GEOJSON file, and compress that file to a reasonable size.

```shell
python download_pumas.py
python consolidate_pumas.py
```

The following scripts download the ACS PUMS data and run the required analysis on them.

```shell
python download_pums.py
python analyze_pums.py
```

Once the data is downloaded and modified, you will be able to run the dashboard locally. Simply run:

```shell
python dashboard.py
```

The dashboard will be available locally at [http://127.0.0.1:8050/]().

## Overview of Data Sources

This dashboard uses data from the [American Community Survey (ACS)](https://www.census.gov/programs-surveys/acs), a yearly survey by the United States Census Bureau. Specifically, the dashboard uses the ACS [Public Use Microdata Sample (PUMS)](https://www.census.gov/programs-surveys/acs/microdata.html), a high resolution, anonymized sample of individuals and households across every participating state and entity. 

This dashboard uses the [ACS 5-year estimate](https://www.census.gov/data/developers/data-sets/acs-5year.html) PUMS data, because it is much more reliable for geographic areas which are sparsely populated.

PUMS data is organized geographically into [Public Use Microdata Areas (PUMAs)](https://www.census.gov/programs-surveys/geography/guidance/geo-areas/pumas.html), non-overlapping, statistical geographic areas that partition each state or equivalent entity into geographic areas containing no fewer than 100,000 people each.

## Downloading and Setting up Data Files

2019 5-year Summary ACS PUMS Data can be found at the [Census FTP site](https://www2.census.gov/programs-surveys/acs/data/pums/2019/5-Year/). The latest data is available on the Census ['Accessing PUMS Data'](https://www.census.gov/programs-surveys/acs/microdata/access.html) page. Person files are prefaced with 'p', and household files with 'h', followed by a two-letter state abbreviation (for example, person and household files for Vermont would be `csv_pvt.zip` and `csv_hvt.zip` respectively).

**TODO: Create a script which downloads and unzips all PUMS data files, combines the files, runs analysis, and produces minimized dataset files for the dashboard.**

Geographic files for PUMAs can be downloaded from the [US Census Bureau website](https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-line-file.html). 2019 5-year Summary PUMAs can be found on the [Census FTP site](https://www2.census.gov/geo/tiger/TIGER2019/PUMA/). PUMAs are available as [TIGER/Line Shapefiles](https://en.wikipedia.org/wiki/Topologically_Integrated_Geographic_Encoding_and_Referencing).

[GeoJSON](https://geojson.org/) is a geographic data structure file standard. The [Plotly map](https://plotly.com/python/mapbox-county-choropleth/) in this dashboard requires a GeoJSON file as its source, so we must convert ACS PUMAs from shapefiles to GeoJSON. This can be done several ways. The easiest is to use the [Ogre web client](https://ogre.adc4gis.com/).

**TODO: Create a script which downloads all PUMA shapefiles, converts them to GeoJSON files using the Ogre API, and combines them into one big GeoJSON file.**

## Plotly Graphing Libraries & Plotly Dash

This dashboard was written in Python using [Plotly Graphing Libraries](https://plotly.com/graphing-libraries/), and [Plotly Dash](https://dash.plotly.com/), a framework for quickly building interactive dashboards. Dash provides an abstraction layer above a ReactJS single page application (SPA), and requires no knowledge of JavaScript to use. Plotly Graphing Libraries and Plotly Dash can be written in Python, R, or Julia.