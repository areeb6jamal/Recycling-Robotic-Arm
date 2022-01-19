import time
import random
import sys
sys.path.append('../')

from Common_Libraries.p3b_lib import *

import os
from Common_Libraries.repeating_timer_lib import repeating_timer

def update_sim():
    try:
        my_table.ping()
    except Exception as error_update_sim:
        print (error_update_sim)

### Constants
speed = 0.2 #Qbot's speed

### Initialize the QuanserSim Environment
my_table = servo_table()
arm = qarm()
arm.home()
bot = qbot(speed)

##---------------------------------------------------------------------------------------
## STUDENT CODE BEGINS
##---------------------------------------------------------------------------------------
#For reference
pick_up_location = 0.670,0,0.20
drop_off_location1 = -0.1,-0.414,0.55
drop_off_location2 = 0, -0.414, 0.55
drop_off_location3 = 0.1, -0.414, 0.55
#Also for reference but note the program will work regardless of the order of bins
bin1color = "red"
bin2color = "green"
bin3color = "blue"
bin4color = "white"

#Worked on all functions together, both Areeb and Alex

#Function to calculate average
#Used when average color sensing reading is needed
def calc_avg(data):
    total = 0
    for reading in data:
        total += reading
    #Adds all values then divides by the number of values; the average
    return total/len(data)

#Dispense container onto table function
def dispense_container():
    #Generate, store and return the bin id of a random container
    num = random.randint(1,6)
    bin_id = my_table.container_properties(num)[2]
    return bin_id

#Load container from sorting station to qbot function
def load_container(bin_id):
    #The reason the bottle is dropped in the load_container function is because if called in the other
    #function it will leave a bottle on the table once it has a different bin id than the first dropped
    #bottle and the next loop of the program will have a bottle dropping on top of another.
    #This way the loop of the program can ensure no bottle is dropped if there is already one there
    my_table.dispense_container()
    #Set a 3 item list where all values are different
    id_list = [0,1,2]
    #Replace first index with the current dropped container bin id
    id_list[0] = bin_id
    print(id_list)
    #Grab and move container onto qbot, 1st dropoff location
    arm.move_arm(0.670,0,0.20)
    arm.rotate_elbow(-10)
    arm.control_gripper(45)
    arm.move_arm(-0.1,-0.414,0.55)
    arm.rotate_elbow(15.5)
    arm.control_gripper(-27.5)
    arm.rotate_elbow(-18)
    arm.home()
    #Call a 2nd random container remembering this new container bin id
    bin_id = dispense_container()
    #Replace second index with the new container bin id
    id_list[1] = bin_id
    #See the current list
    print(id_list)
    #Check to see if the most recent container has the same bin id as the previously sorted one
    #If it does then move it to dropoff location 2
    #Else do nothing, and move onto to transfering
    if id_list[1] == id_list[0]:
        #Note no bottle will drop if bin ids dont match
        my_table.dispense_container()
        arm.move_arm(0.670,0,0.20)
        arm.rotate_elbow(-10)
        arm.control_gripper(45)
        arm.move_arm(0, -0.414, 0.55)
        arm.rotate_elbow(15.5)
        arm.control_gripper(-27.5)
        arm.rotate_elbow(-18)
        arm.home()
        bin_id = dispense_container()
        id_list[2] = bin_id
        print(id_list)
        #Nested if statement because no need to check a 3rd bottle if the 2nd one was different
        #Check to see if the most recent container has the same bin id as the previously sorted one
        #If it does then move it to dropoff location 3
        #Else do nothing, and move onto to transfering
        if id_list[2] == id_list[1]:
            my_table.dispense_container()
            arm.move_arm(0.670,0,0.20)
            arm.rotate_elbow(-10)
            arm.control_gripper(45)
            arm.move_arm(0.1, -0.414, 0.55)
            arm.rotate_elbow(15.5)
            arm.control_gripper(-27.5)
            arm.rotate_elbow(-18)
            arm.home()
    
#Transfer container to appropriate bin function
def transfer_container(bin_id):
    #See where the qbot should go to
    print("Going to " + bin_id)
    #Move to first white+yellow line intersection and rotate to face bin
    bot.forward_time(4.25)
    #Told to stop before turning to get more precise rotations
    bot.stop()
    #Qbot doesnt rotate a perfect 90 degrees so a larger angle is inputted
    bot.rotate(91.5)
    bot.stop()
    #Activate, store and read all color sensors
    bot.activate_color_sensor("Red")
    reading_red = bot.read_red_color_sensor("Bin01",0.5)
    bot.activate_color_sensor("Green")
    reading_green = bot.read_green_color_sensor("Bin02",0.5)
    bot.activate_color_sensor("Blue")
    reading_blue = bot.read_blue_color_sensor("Bin03",0.5)
    #Find the averages of the readings
    avg_reading_red = calc_avg(reading_red)
    avg_reading_green = calc_avg(reading_green)
    avg_reading_blue = calc_avg(reading_blue)
    #Check if the current bin is the right bin
    if bin_id == "Bin01" and avg_reading_red > 4:
        #Stop and break out of function if it is the correct bin
        bot.stop()
        print("Correct Bin!")
        return "Red"
    #If it the wrong bin, move on to check the next bin
    else:
        print("Wrong Bin")
        #Travel to 2nd bin location
        bot.rotate(-90)
        bot.stop()
        bot.forward_time(2.2)
        bot.stop()
        bot.rotate(91.5)
        #Repeat bin check
        bot.activate_color_sensor("Red")
        reading_red = bot.read_red_color_sensor("Bin01",0.5)
        bot.activate_color_sensor("Green")
        reading_green = bot.read_green_color_sensor("Bin02",0.5)
        bot.activate_color_sensor("Blue")
        reading_blue = bot.read_blue_color_sensor("Bin03",0.5)
        avg_reading_red = calc_avg(reading_red)
        avg_reading_green = calc_avg(reading_green)
        avg_reading_blue = calc_avg(reading_blue)
        #Bin 2 is green
        if bin_id == "Bin02" and avg_reading_green > 4:
            bot.stop()
            print("Correct Bin!")
            return "Green"
        #If it the wrong bin, move on to check the next bin
        else:
            #Travel to 3rd bin location
            print("Wrong Bin")
            bot.rotate(-90)
            bot.stop()
            bot.forward_time(2.15)
            bot.stop()
            bot.rotate(91.5)
            #Repeat bin check
            bot.activate_color_sensor("Red")
            reading_red = bot.read_red_color_sensor("Bin01",0.5)
            bot.activate_color_sensor("Green")
            reading_green = bot.read_green_color_sensor("Bin02",0.5)
            bot.activate_color_sensor("Blue")
            reading_blue = bot.read_blue_color_sensor("Bin03",0.5)
            avg_reading_red = calc_avg(reading_red)
            avg_reading_green = calc_avg(reading_green)
            avg_reading_blue = calc_avg(reading_blue)
            if bin_id == "Bin03" and avg_reading_blue > 4:
                bot.stop()
                print("Correct Bin!")
                return "Blue"
            #If it the wrong bin, move on to check the next bin
            else:
                #Travel to final bin location
                print("Wrong Bin")
                bot.rotate(-90)
                bot.stop()
                bot.forward_time(2.0)
                bot.stop()
                bot.rotate(91.5)
                #Repeat bin check
                bot.activate_color_sensor("Red")
                reading_red = bot.read_red_color_sensor("Bin01",0.5)
                bot.activate_color_sensor("Green")
                reading_green = bot.read_green_color_sensor("Bin02",0.5)
                bot.activate_color_sensor("Blue")
                reading_blue = bot.read_blue_color_sensor("Bin03",0.5)
                avg_reading_red = calc_avg(reading_red)
                avg_reading_green = calc_avg(reading_green)
                avg_reading_blue = calc_avg(reading_blue)
                #If none of the sensors detect anything we know it is a white bin which is bin 4
                if bin_id == "Bin04" and avg_reading_red < 1 and avg_reading_green < 1 and avg_reading_blue < 1:
                    bot.stop()
                    print("Correct Bin!")
                    return "Blue"
#Deposit container into correct bin function 
def deposit_container():
    #Move forward until near bin
    bot.travel_forward(0.20)
    #Dump bottles in bin
    bot.stop()
    bot.rotate(-89.5)
    bot.activate_actuator()
    bot.dump()

#Bring qbot back to home position function
def return_home():
    #Exit out of dump bin location
    bot.rotate(-92)
    bot.forward_time(1.3)
    #Face away from home position
    bot.rotate(90)
    lost_line = 0
    #Collect and update the number of lost yellow lines from follow_line 
    #Velocity needed to bring the qbot back on the line is inputted to continue following the line
    while lost_line < 2:
        lost_line, velocity = bot.follow_line(0.3)
        bot.forward_velocity(velocity)
    #The above while loop brings it near the home position but not exactly
    #Adjustments to bring the qbot exactly home and facing the correct direction
    bot.forward_time(0.291)
    bot.rotate(193.125)

#Main function which calls all functions
def main():
    #Infinite loop to run however many times
    i = 1
    while i > 0:
        #Call dispense and load qbot functions
        bin_id = dispense_container()
        load_container(bin_id)
        #The first bin id is going to be the transfer location so transfer container function is
        #called with the parameter of the first bin id
        transfer_container(bin_id)
        deposit_container()
        return_home()
       
main()


##---------------------------------------------------------------------------------------
## STUDENT CODE ENDS
##---------------------------------------------------------------------------------------
update_thread = repeating_timer(2,update_sim)
