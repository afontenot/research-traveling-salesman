import json
import polyline

with open("route.json") as f:
    j = json.load(f)

for route in j["routes"]:
    print(f"route for vehicle {route['vehicle']}:")
    for step in route['steps']:
        print(step['location'])
    print()

    geo = route["geometry"]
    geojson = polyline.decode(geo, geojson=True)

    with open(f"route{route['vehicle']}.txt", 'w') as f:
        for line in geojson:
            f.write(','.join([str(x) for x in line]) + '\n')


