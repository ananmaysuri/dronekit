print "Start simulator (SITL)"
import dronekit_sitl
import math
sitl = dronekit_sitl.start_default()
connection_string = sitl.connection_string()

from dronekit import connect, VehicleMode

print("Connecting to vehicle on: %s" % (connection_string,))
vehicle = connect(connection_string, wait_ready=True)

print "Get some vehicle attribute values:"
print " GPS: %s" % vehicle.gps_0
print " Battery: %s" % vehicle.battery
print " Last Heartbeat: %s" % vehicle.last_heartbeat
print " Is Armable?: %s" % vehicle.is_armable
print " System status: %s" % vehicle.system_status.state
print " Mode: %s" % vehicle.mode.name

def arm_and_takeoff(aTargetAltitude):
    print "Basic pre-arm checks"
    while not vehicle.is_armable:
        print " Waiting for vehicle to initialise..."
        time.sleep(1)
    print "Arming motors"
    vehicle.mode    = VehicleMode("GUIDED")
    vehicle.armed   = True
    while not vehicle.armed:
        print " Waiting for arming..."
        time.sleep(1)
    print "Taking off!"
    vehicle.simple_takeoff(aTargetAltitude)
    while True:
        print " Altitude: ", vehicle.location.global_relative_frame.alt
        if vehicle.location.global_relative_frame.alt>=aTargetAltitude*0.95:
            print "Reached target altitude"
            break
        time.sleep(1)

arm_and_takeoff(1)

def goto(dNorth, dEast, gotoFunction=vehicle.simple_goto):
    currentLocation=vehicle.location.global_relative_frame
    targetLocation=get_location_metres(currentLocation, dNorth, dEast)
    targetDistance=get_distance_metres(currentLocation, targetLocation)
    gotoFunction(targetLocation)

    while vehicle.mode.name=="GUIDED":
        remainingDistance=get_distance_metres(vehicle.location.global_frame, targetLocation)
        print "Distance to target: ", remainingDistance
        if remainingDistance<=targetDistance*0.01:
            print "Reached target"
            break;
        time.sleep(2)

def circle(r):
    print("Set groundspeed to 5m/s.")
    vehicle.groundspeed = 5
    for i in range(360):
        yaw = vehicle.heading
        time.sleep(1)
        x = x+r*math.cos(yaw+1)
        y = y+r*math.sin(yaw+1)
        goto(r*x,r*y)

circle(1)

def land():
    print("Setting LAND mode...")
    vehicle.mode = VehicleMode("LAND")

vehicle.close()

sitl.stop()
print("Completed")
