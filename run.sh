# first create a coords.dat file
# creates the tasks.json
python makejson.py
# calculates optimal routes; server needs to be running OSRM with all relevant map data
# jq is technically optional but very helpful because it will pretty print the JSON
~/Programs/vroom/bin/vroom -i tasks.json -g -a myserver -p 5000 | jq . > route.json
# reads route.json and writes routes and puts geometry coords in route#.txt
python readroute.py
