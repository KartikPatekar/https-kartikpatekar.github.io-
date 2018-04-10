# ITSP 2017 Team 16  "Autonomous Bot"

## **Problem Statement:**
To build a self-navigating bot which reaches its destination while avoiding obstacles in its way.

## Introduction:
We made a bot which can go from one geographical coordinate to another automatically using GPS mapping, avoiding basic obstacles on its way. The bot is provided the final location(coordinates) on the map and it follows the shortest route to reach that location. The bot uses a combination of ultrasonic and sharp sensors to avoid basic obstacles in its way. 
Such a bot has many applications in daily life. On further advancements, 

## Motivation: 
Automation had always attracted humans. Delivering something to a friend urgently can really become a troublesome due to lack of time, so we set out to make an autonomous bot was to make something that can be used to deliver stuff over long distances without any human intervention. 
Upon further modifications, such a bot can have great applications. It can be used as unmanned delivery vehicle, in warfare, in carrying out some tasks in difficult terrain, etc. It can also be treated as a miniature version of google driverless car. Using appropriate sensors, the bot can also be used in rescue operations in times of natural disasters.

-----------------------------------------------------------------------------------------------------------------

**Main Components of our bot:**
1.	GPS receiver module (Neo-6m)
2.	GSM/GPRS module (Sim800)
3.	Sharp Sensor(Gp2y0a21yk0f)
4.	Arduino Uno
5.	Ultrasonic Sensor (HCSR04)
6.	Magnetometer 


### GPS receiver module:

The Global Positioning System (GPS) is a network of about 30 satellites orbiting the Earth at an altitude of 20,000 km. At least four GPS satellites are ‘visible’ at any time at any place on the planet, which sends data to GPS receiver to pin point its position using “Trilateration” (ref : http://www.mio.com/technology-trilateration.htm) 
“tinyGPS” is a very useful arduino library to extract the useful data from the GPS. The main code for calculating position using GPS is given below :
(Here, ‘myserial’ is a SoftwareSerial object for GPS module.)
    
    int gpsdata(float &flat, float &flon)
      {
         bool newdata=0;
         while (!newdata) 
         {
           if (mySerial.available()) 
           {
   	      char c = mySerial.read();
              //Serial.print(c);  // uncomment to see raw GPS data
              if (gps.encode(c)) 
       	      {
                 newdata = true;
         	 break;  // uncomment to print new data immediately!
       	      }
           }
         }

         if(!newdata)
         return 0;
         unsigned long age;
         gps.f_get_position(&flat, &flon, &age);   
         return 1;
      }


### GSM/GPRS module:
 A GSM module or a GPRS module is a chip or circuit that will be used to establish communication between a mobile device or a computing machine and a GSM or GPRS system. General Packet Radio Service (GPRS) is a packet oriented mobile data service on the 2G and 3G cellular communication system’s global system for mobile communications (GSM). 
The path is calculated on a local machine and a html file containing the coordinates of points on the calculated path is uploaded on a webserver which is accessed by mobile GPRS module to provide the coordinates to the bot in real time. The nth line on the html file contains coordinates of the nth point in its path. 

### Sharp Sensor

The detector in the Sharp IR sensor is similar to the imaging sensor found in digital cameras. Since the detector and the IR LED have a fixed distance and orientation relative to each other, the distance of an object will affect the angle at which the light from the IR LED hits the receiver. By looking at where the light hits the detector, it is possible to calculate the angle of the light and from that angle derive the distance to the object (all of which is done by the sensor itself).
Code for distance calculation:   

**Working Of Sharp Sensor**

![Sherp Sensor](https://github.com/KartikPatekar/ITSP16/blob/master/Sharp%20sensor.png)


The bot uses a servo motor to rotate the sharp sensor by 180 degrees to get accurate measurement of all the obstacles around the bot.`

### Ultrasonic Sensor`
An Ultrasonic sensor is a device that can measure the distance to an object by using sound waves. It measu`res distance by sending out a sound wave at a specific frequency and listening for that sound wave to bounce back. By recording the elapsed time between the sound wave being generated and the sound wave bouncing back, it is possible to calculate the distance between the sonar sensor and the object.

### Arduino communication
Since the bot has 4 ultrasound sensor, a sharp sensor, a servo motor, a magnetometer, GPS receiver and GSM/GPRS module, it needs 2 arduinos to control all these devices. The two arduinos communicate with each other using serial i2c communication. The slave Arduino hosts the GPS receiver and GSM/GPRS module, while remaining devices are operated by master arduino.

*********

## Milestone achieved 
1.	Path Calculation
2.	Path following bot
3.	Obstacle avoiding bot

### Path Following bot
An HTML file containing the calculated map points is hosted on a free webserver. The mobile bot can access this html file using GPRS and can acquire the path from a remote location. The bot then matches its heading with the required direction using magnetometer, and then moves towards its destination.
Obstacle avoiding bot
The bot has been equipped with an infrared proximity sensor (SHARP 2Y0A02) along with four ultrasonic sensors (HCSR04 modules).
The proximity sensor (SHARP Sensor ) is mounted on a servo motor (9gr) making it/which has been denoted here as SHARP-SERVO mechanism. The panoramic range has been kept to 120 degrees symmetrically in the forward direction.
The mechanism has been coded to effectively avoid all stationery/ slow moving obstacles which subtend at least ~ 10 degrees (neglecting error) on the sensor.
The error observed was significantly less and its effect has been effectively submerged by keeping a higher limit of 10 degrees on the sides and 6 degrees in the front. The ultrasonic sensors are kept (two in front and two at ~ 45 degrees from the front facing either sides) to tell the bot when to start the SHARP-SERVO mechanism to be able to avoid obstacles. As soon as any of the ultrasound sensors detect an obstacle (at max 40 cm from the bot). The code for the obstacle avoidance using SHARP-SERVO mechanism begins and continues till none of the ultrasonic sensors detect the obstacle beyond which the code proceeds to the path following mode (provided by GPS and magnetometer compass).

### The final bot
In each iteration of the “void loop()” the bot calculates its present GPS coordinate, and the distance of obstacles around it using ultrasonic sensor. The bot then decides whether to focus on following the path or avoiding obstacles.

Code for "void loop()" in master arduino:

    void loop()
    { 
         gpsdata(latgps, lnggps);
         if(lat[i]-2*elat<latgps && latgps<lat[i]+2*elat && lng[i]-2*elng<lnggps && lnggps<lng[i]+2*elng)
         {
           i++; 
         }

         else{
               if(dist(leftf)>20 && dist(rightf)>20 && dist(frontl)>40 && dist(frontr)>40 )
               {
                  follow_path(i,latgps,lnggps);
               }
               else
               {
                  avoid_obstacle();  
               }
            }
       
    }

**Sensor positions on the bot**

![Sensor Positioning](https://raw.githubusercontent.com/KartikPatekar/ITSP16/master/Sensor%20Position.png)                       
