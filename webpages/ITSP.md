# ITSP 2017 Team 16  "Autonomous Bot"

## **Problem Statement:**
To build a self-navigating bot which reaches its destination while avoiding obstacles in its way.

## Introduction:
We made a bot which can go from one geographical coordinate to another automatically using GPS (for its current location) and a map scaled to coordinates (latitude and longitude). The bot avoids stationary or slowly moving obstacles on its way. The bot is provided the final location(coordinates) on the map and it follows the shortest route to reach that location. The bot uses a combination of ultrasonic and sharp sensors to avoid basic obstacles in its way. 
Upon further modifications, such a bot can have great applications. It can be used as unmanned delivery vehicle, in warfare, in carrying out some tasks in difficult terrain, etc. It can also be treated as a miniature version of google driverless car. Using appropriate sensors, the bot can also be used in rescue operations in times of natural disasters.

## Motivation: 
Automation had always attracted humans. Delivering something to a friend urgently can really become a troublesome due to lack of time, so we set out to make an autonomous bot was to make something that can be used to deliver stuff over long distances without any human intervention. 


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

     int distance() 
     {
        float proxSens = analogRead(A1);
        float volts = proxSens * VPU; // ("proxSens" is from analog read)
        float cm = 60.495 * pow(volts, -1.1904);  // same in cm
 
        if (volts < .2 || cm>80)
        {
          cm = 1000.0;
        }     // out of range

        return cm;
      }
      
**Working Of Sharp Sensor**

![Sherp Sensor](https://github.com/KartikPatekar/ITSP16/blob/master/Sharp%20sensor.png)


The bot uses a servo motor to rotate the sharp sensor by 180 degrees to get accurate measurement of all the obstacles around the bot.

### Ultrasonic Sensor
An Ultrasonic sensor is a device that can measure the distance to an object by using sound waves. It measures distance by sending out a sound wave at a specific frequency and listening for that sound wave to bounce back. By recording the elapsed time between the sound wave being generated and the sound wave bouncing back, it is possible to calculate the distance between the sonar sensor and the object.

### Arduino communication
Since the bot has 4 ultrasound sensor, a sharp sensor, a servo motor, a magnetometer, GPS receiver and GSM/GPRS module, it needs 2 arduinos to control all these devices. The two arduinos communicate with each other using serial i2c communication. The slave Arduino hosts the GPS receiver and GSM/GPRS module, while remaining devices are operated by master arduino.

*********

## Milestone achieved 
1.	Path Calculation
2.	Path following bot
3.	Obstacle avoiding bot

### Path Calculation
**How to get desired map from Google map**

>1.Google map API
It gives the flexibility to get the desired map from google maps like we wanted a map with no labels on it and narrow roads. There were numerous way in which we can create the map. To get the image of map we used static map API which only needs the centre coordinate of the map,zoom level and pixel dimension of the static image of map required.You can have a look on this site for it. "[Google Styling Wizard](https://mapstyle.withgoogle.com/)"

>2.OpenCV to improve map image
Opencv is a c++ library which helps to process images. It converts image into a 3 Dimensional array of pixels containing values representing weights of Red, Blue, Green color in terms of integers ranging from 0 to 255. This tutorial helped me to use OpenCV. But we used grayscale image which is converted into 1 Dimensional array conataining integer values representing weight of white color of a pixel(0 meant black,255 meant white). As the image generated from Google API didn't gave us an image which can be directly used to find shortest path. So, by observing the values of pixel for road and surrounding we converted the map image into an image which has black colored pixels as road and other things having different color. [OpenCv](http://opencv.org/)

>3.Latitude longitude from google maps
After fixing the map zoom level we noted down the change in latitude and longitude for a fixed number of pixels. We got the change in latitude per pixel and longitude per pixel and as we know the centre coordinate of the map using ratio proportion we calculated latitude and longitude of each and every pixel on the image.




**Algorithm to find shortest path between initial and final coordinates**
>let color of pixel for road be black.

1.Feed in initial and final lat and lng using which we get pixel coordinates on road of the map.(It might happen that pixel is not of road. So below written code makes sure that we get on a nearby road pixel.)

2.Make an array of pixels around the present pixel which have color of road and color the present pixel white.["Around" here means a square of 3x3 pixels having center at present pixel]

3.Calculate distance of each pixel from the final position, one having minimum distance is then considered as present pixel , after that go back to step 2.Simultaneously update the value of two vectors one with x coordinate another with y coordinates of pixels which have been whitened.

4.While doing step 2 & 3 it might happen that there is no pixel having color of road with center at present pixel around it, then go back to previous whitened pixel until a pixel of color of road is found then go back to step 2.Simultaneously remove the coordinates of the white pixel which it has retraced.However the color of the pixel which retraces remain same.

5.There are two other vectors of int type which stores all the pixels which have been whittened.So at last when it reaches its final point we color all the whitened pixels to black and then use the vectors which have been updated in step 2,3&4 to color the path white from initial to final position.

    vector<int> xp,yp,xpn,ypn,abc,efg;
    vector<float> lng,lat;  
    while(x!=xf || y!=yf){
        int a[8][2];
        int d[8];
        int b=0;
        for(int i=-1;i<2;i++){
            if(i==0){
                for(int j=-1;j<2;j+=2){
                    if(img.at<int8_t>(x+i,y+j)==0){
                        a[b][0]=x+i;
                        a[b][1]=y+j;
                        b++;
                    }
                }
            }
            else{
                for(int j=-1;j<2;j++){
                    if(img.at<int8_t>(x+i,y+j)==0){
                        a[b][0]=x+i;
                        a[b][1]=y+j;
                        b++;
                    }
                }
            }
        }
        if(b==0){
            if(xp[xp.size()-1]==x && yp[yp.size()-1]==y){
                lat.pop_back();
                lng.pop_back();
                xp.pop_back();
                yp.pop_back();
                abc.pop_back();																//
                efg.pop_back();																//
            }else{
                img.at<int8_t>(x,y)=255;
                xpn.push_back(x);
                ypn.push_back(y);
            }
            x=xp[xp.size()-1];
            y=yp[yp.size()-1];
            continue;
        }

        for(int i=0;i<b;i++){
            d[i]=(xf-a[i][0])*(xf-a[i][0])+(yf-a[i][1])*(yf-a[i][1]);
        }
        int m=d[0];
        int in=0;
        for(int i=1;i<b;i++){
            if(m>d[i]){
                m=d[i];
                in=i;
            }
        }

        img.at<int8_t>(x,y)=255;
        xp.push_back(x);
        yp.push_back(y);
        abc.push_back(x);																	//
        efg.push_back(y);																	//
        xpn.push_back(x);
        ypn.push_back(y);
        lat.push_back(clat+(200-x)*latppx);
        lng.push_back(clng+(y-200)*lngppx);

        x=a[in][0];
        y=a[in][1];
    }
   


### Path Following bot
An HTML file containing the calculated map points is hosted on a free webserver. The mobile bot can access this html file using GPRS and can acquire the path from a remote location. The bot then matches its heading with the required direction using magnetometer, and then moves towards its destination.
### Obstacle avoiding bot
The bot has been equipped with an infrared proximity sensor (SHARP 2Y0A02) along with four ultrasonic sensors (HCSR04 modules).
The proximity sensor is mounted on a servo motor (9gr) which has been denoted here as SHARP-SERVO mechanism. The panoramic range has been kept to 120 degrees symmetrically in the forward direction.
 The mechanism has been coded to effectively avoid all stationary/ slow moving obstacles which subtend at least ~ 10 degrees (neglecting error) on the sensor.
The error observed was significantly less and its effect has been effectively submerged by keeping a higher limit of 10 degrees on the sides and 6 degrees in the front. 
 The ultrasonic sensors are kept (two in front and two at ~ 45 degrees from the front facing either sides) to tell the bot when to start the SHARP-SERVO mechanism to be able to avoid obstacles. As soon as any of the ultrasound sensors detect an obstacle at max 40 cm from the bot the code for the obstacle avoidance using SHARP-SERVO mechanism begins and continues till none of the ultrasonic sensors detect the obstacle beyond which the code proceeds to the path following mode (provided by GPS and magnetometer compass).

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

### References:
1. https://www.arduino.cc/en/Tutorial/HomePage
2. https://github.com/mechasolution/Mecha_QMC5883
3. http://www.instructables.com/id/Connecting-GPS-module-to-Arduino/
4. https://www.google.co.in
5. http://docs.opencv.org/2.4/doc/tutorials/tutorials.html
