import csv
import json

## Note: these data structures are immutable, but using list
# for easy incorporation into JSON

# description of vehicles with passenger skills
# note: 0 is a reserved skill, due to a bug in an underlying library
VEHICLES = [[1]]

# lists of start and end points for each car
STARTCOORDS = [[-118.44, 34.068]] # lon, lat
ENDCOORDS = [[-118.44, 34.068]] # lon, lat

# because vroom only supports minimizing work-time, not real-time,
# we have to slowly reduce the working hours value until we get
# something reasonable that splits the work between vehicles.
TIMEAVAIL = [400000] # seconds


# start building json
j = {}

j_vehicles = []
for i, (vehicle, s_coord, e_coord, t_avail) in enumerate(zip(VEHICLES, STARTCOORDS, ENDCOORDS, TIMEAVAIL)):
    j_vehicle = {}
    j_vehicle["id"] = i + 1
    j_vehicle["start"] = s_coord
    j_vehicle["end"] = e_coord
    j_vehicle["skills"] = vehicle
    # append dummy skill because of 
    # https://github.com/VROOM-Project/vroom/issues/460
    j_vehicle["skills"].append(0)
    # work around lack of a real-time minimization strategy
    j_vehicle["time_window"] = [0, t_avail]
    j_vehicles.append(j_vehicle)
j["vehicles"] = j_vehicles

# each line in coords.dat is a tab-delimited job:
# LAT<tab>LON<tab>SKILLS<tab>TIME
# Entries with SKILLS must be numbers corresponding to vehicles descriptions.
# Entries with TIME take an arbitrary positive TIME to complete (in seconds).

with open('coords.dat', newline='') as f:
    reader = csv.reader(f, delimiter='\t')
    j_tasks = []
    for i, line in enumerate(reader):
        # parse line
        lat, lon = float(line[0]), float(line[1])
        skills = [0]
        task_duration = None
        if len(line) >= 3:
            skills = line[2]
            if ',' in skills:
                skills = [int(x) for x in skills.split(',')]
            elif skills == "":
                skills = [0]
            else:
                skills = [int(skills)]
        if len(line) == 4:
            task_duration = int(line[3])

        # craft task json
        j_task = {}
        j_task["id"] = i + 1
        if task_duration:
            j_task["service"] = task_duration
        j_task["location"] = [lon, lat]
        j_task["skills"] = skills

        # add to task list
        j_tasks.append(j_task)

j["jobs"] = j_tasks

with open("tasks.json", 'w') as f:
    json.dump(j, f)
