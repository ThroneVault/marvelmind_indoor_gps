# marvelmind robotics indoor gps

This is a ROS package for the [Indoor GPS](docs/more_words.md) kit from Marvel Mind robotics, providing indoor localization for robots. This is adapted from software written by Boris Zinin (b.zinin@gmail.com)

![alt tag](http://www.marvelmind.com/pics/marvelmind_indoor_GPS.png)

The kit comes with 5 beacons. Four of the beacons are installed on a wall or an open location, and one of them, called the hedgehog, is installed on a mobile robot for tracking (you can set the hedgehog using the marvel mind [software](http://www.marvelmind.com/#Download)).   

To run the package, first open the marvel mind software, turn on all the beacons, set one of the as the hedgehog, and then freeze the map. You should hear the hedgehog start ticking. Read the manual [here](http://www.marvelmind.com/pics/marvelmind_navigation_system_manual.pdf) for detailed instructions on this. Next, connect the hedgehog to the microcontroller or labtop on your robot using the micro-usb cable.

For a quick test, edit the `indoor_gps.launch` file with the correct port for the hedge hog (e.g. /dev/ttyACM0, etc.), then run
``` 
roslaunch marvelmind_indoor_gps indoor_gps.launch
```

The (x,y) coordinates of hedgehog are published to a topic named indoor_gps.
