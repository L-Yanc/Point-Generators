#! /usr/bin/env python
import rospy
import json
from geometry_msgs.msg import Pose, TransformStamped
from sensor_msgs.msg import Joy

Trigger = False
Trigger2 = False
name = 'loc'
shelf_name = '02'
shelf_nm = '-1'
data = {}
data[name] = []
number = 1
txt = 1
side = ''
reverse = ''

print("Dosya numarası: ", txt)

def callback(msg):
    global Trigger,number
    while(Trigger) :
        print("Evet, oduncu!")
        number_str = str(number)
        zero_filled_number = number_str.zfill(2)
        data[name].append({
            'SAP_Location' : shelf_name + "-" + zero_filled_number + "-1",
            'position' : {"x":msg.transform.translation.x, "y":msg.transform.translation.y,"z":msg.transform.translation.z},
            'orientation' : {"x":msg.transform.rotation.x,"y":msg.transform.rotation.y,"z":msg.transform.rotation.z,"w":msg.transform.rotation.w}
        })
        number -= 20
        Trigger = False

def joy_callback(key) :
    global Trigger, Trigger2, txt, number,data, name, side, reverse
    if key.buttons[0] == 1 and Trigger2 == True:
        Trigger2 = False
        txt -= 1
        #number = 1
        print("Dosya numarasını değiştirdiniz, güncel dosya numarası: ", txt)    
    elif key.buttons[3] == 1 and Trigger2 == True:
        Trigger2 = False
        txt += 1
        #number = 1
        print("Dosya numarasını değiştirdiniz, güncel dosya numarası: ", txt)    
    elif key.buttons[2] == 1 and Trigger2 == True:
        Trigger2 = False
        reverse = 'r'
        #number = 1
        print("Koridora tersten girdin")
    elif key.axes[2] == -1.0 and Trigger2 == True:
        Trigger2 = False
        side = 'B'
        #number = 1
        print("Current side : ", side)
    elif key.axes[7] == 1.0:
        Trigger2 = True
    elif key.axes[5] == -1.0 and Trigger2 == True:
        Trigger2 = False
        side = 'A'
        #number = 1
        print("Current side : ", side)
    elif key.buttons[5] == 1 and Trigger == False:
        rospy.sleep(1)
        Trigger =  True
    elif key.buttons[4] == 1 and Trigger2 == True:
        rospy.sleep(1)
        Trigger2 = False
        print("Tamam, anladım!")
        with open(str(txt) + side + reverse, 'w') as outfile: #sadece burayı degistir koridor numarası girilecek
            json.dump(data, outfile, indent=2)
            data = {}
            data[name] = []
            reverse = ''
            quit()

def main() :
    rospy.init_node('collect_odometry')
    odom_sub = rospy.Subscriber('/map_to_base_link', TransformStamped, callback)
    joy_sub = rospy.Subscriber('/joy', Joy, joy_callback )
    rate = rospy.Rate(10)
    rospy.spin()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
