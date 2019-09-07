# IoT Plant Monitoring Workshop
<img src=documentation/images/kit.jpg width=600>
Welcome to the Plant Monitoring Workshop! Today we will learn some basic electronics and create a wifi-based plant monitoring device witch measures soil moisture and also ambient temperature, humidity and light.

If you want another kit or need some spare parts, there are links to all the components in the [shopping list](documentation/shopping-list.md).

## Electric Safety
* The kit used in this workshop operates at 5 Volts and below. This means there is no risk for electric shocks, however incorrect use may still break the components themselves.
* Do not put the electronics on conducting surfaces such as metal laptops, powerbanks or other things made from metal.
* Always disconnect power before changing the wiring.
* Double check wiring before connecting power to avoid breaking the components.

## Preparations
<img src=documentation/images/hardware.png width=500>

*Image: [DIY More on Aliexpress](https://www.aliexpress.com/item/32860958750.html)*

The main circuit board contains the popular Espressiff ESP32 module. It has built-in wifi and Bluetooth connectivity, and is [compatible](https://github.com/espressif/arduino-esp32) with the popular [Arduino echosystem](https://www.arduino.cc/en/Guide/Introduction). Today however, we are trying out [Micropython](https://micropython.org/), a custom microcontroller firmware that runs a small Python interpreter so that we can program our ESP32 in Python. 

The boards have already been prepared with Micropython, so all we need to use it is some software on our computer:

1. Install the CP201x USB Driver.
	* [OS X](http://www.silabs.com/Support%20Documents/Software/Mac_OSX_VCP_Driver.zip)
	* [Windows](http://www.silabs.com/Support%20Documents/Software/CP210x_Windows_Drivers.zip)
	* [Linux](http://www.silabs.com/Support%20Documents/Software/Linux_3.x.x_VCP_Driver_Source.zip)
	* [Other](http://www.silabs.com/products/mcu/pages/usbtouartbridgevcpdrivers.aspx)
	
	**Note:** Mac users may need to go in to `System preferences > Security & Privacy > General` and click `Allow` to let the driver run.

2. Install the Visual Studio Code (VSCode) editor:
  https://code.visualstudio.com/Download

3. Install NodeJS, it is required by the plugin in the next step:
  https://nodejs.org/

4. Install the Pymakr plugin for VSCode. It is made for [Pycom](https://pycom.io/) products but works with any Micropython board:
  https://marketplace.visualstudio.com/items?itemName=pycom.Pymakr

5. Click `All Commands` at the bottom of the window in VSCode and then select `Global Setting` in the menu that appears. (If you do not see the Pymakr buttons, try restarting VSCode.)

    <img src=documentation/images/global-settings.png width=500>

    This will open a configuration file. Scroll down to `"autoconnect_comport_manufacturers": [` and add `"Silicon Labs"` to the end of the list. Remember to also add a comma to the end of the second last entry. It should now look like this:

    ```
    "autoconnect_comport_manufacturers": [
      "Pycom",
      "Pycom Ltd.",
      "FTDI",
      "Microsoft",
      "Microchip Technology, Inc.",
      "Silicon Labs"
    ]
    ```
    Don't forget to save the file after you make the change!

6. Connect your board to a USB port. Be careful to not place the board on metal as the pins may short out and break it.

7. In VSCode, if you do not see a terminal in the lower portion of your window, click `Pycom Console` in the status bar.

    <img src=documentation/images/pycom-console.png width=500>

8. In the terminal, there should be a Pycom Console with a Python REPL (indicated by the symbols `>>>`). If there is some error about not finding the board, click the trash can symbol <img src=documentation/images/trash.png width=30px>. Pymakr will open another console and should now find the board.

    <img src=documentation/images/restart-console.png width=500>
    <img src=documentation/images/console-open.png width=500>

## 1. Blink a light
Now we are ready to run a simple test to make sure everything is working.

1. Write the following in the Pycom Console:
    ```
    >>> from machine import Pin, Signal
    >>> led = Signal(16, Pin.OUT, invert=True)
    >>> led.on()
    >>> led.off()
    ```
    You should see the blue LED turn on and off with each corresponding command.

2. Download the code examples from this repository:
  https://github.com/albertskog/iot-workshop-plant-monitoring/archive/master.zip

3. In the VSCode file explorer, click `Add folder` and open `1-blink-a-light` from the zip file that you just downloded. You should now see `main.py` in the side panel, click to open it.

    <img src=documentation/images/open-folder.png width=500>


4. To run the code without saving it on the board, press `⌘-Shift-R` or `Ctrl-Shift-R`. You should see the blue LED start blinking once per second. If you press `Ctrl-C` in the Pycom Console or reset the board, the blinking stops. This is useful for testing.

5. To save the code to the board instead, press `⌘-Shift-S` or `Ctrl-Shift-S`. (You can also press `Upload` at the bottom of the window.) It will now resume blinking even if you disconnect the board and plug it back in.

**Note:** that the Pymakr plugin will get confused if you have multiple folders open in the same VSCode window and upload all of them to the device.

**Note:** you can find all VSCode commands and their shortcuts by pressing `⌘-Shift-P` or `Ctrl-Shift-P`. Type `Pymakr` to show the relevant commands and select with the arrow keys. If you can only remember one hotkey, this should be the one!

**Bonus:** try changing the delays and adding in more lines to create other blinking patterns.


## 2. Print a message
It is sometimes helpful to print out a message to yourself to figure out what the code is doing. Try out this program and see if you understand how it works. Create a new file in VSCode, paste the code below and save it as `main.py` inside a new folder, then press Upload. After uploading, have a look at the output in the Pycom Console.

```python
from time import sleep

message_number = 0

while True:
  print("This is message number {}".format(message_number))
  message_number += 1
  sleep(1)
```

You should see messages appearing once per second:

```
>>> Running main.py
>>> 
This is message number 0
This is message number 1
This is message number 2
This is message number 3
```
**Note:** Micropython looks for a file called `main.py` when it starts. If you named yours differently, it will run the last `main.py` that you uploaded.

**Bonus:** try to only update the number without printing a whole new line!

## 3. Get connected
The hardware is working, now let's make it talk to the Internet! For today, we will use an existing IoT platform to play with the data, but it could of course also be sent to your own app or website.

1. Go to https://maker.allthingstalk.com and sign up for an account.

2. Log in, press `Connect a device` and select `Your own device`.

3. Each device can have many different sensors, or "assets". Add a new asset to your device by clicking `Create asset`. Call the asset `counter` (important!) and set the type to `Integer`.

	You should now end up at you device page with one asset called `counter`. As you can see, your brand new counter has the value `--`. Let's fix that!

4. In VSCode, open the folder `3-counter`. The file explorer on the left should show three files; `allthingstalk.py`, `config.py` and `main.py`, 

5. Open `config.py` and replace `XXXXXX` with proper values.
  
    ```python
    config = {
      "wifi_ssid": "XXXXXX",
      "wifi_password": "XXXXXX",
      "device_id": "XXXXXX",
      "device_token": "maker:XXXXXX",
    }
    ```

	Device ID and token can be found in AllThingsTalk. Go to your device page and click `Settings` in the top right corner, then `Authentication`.

6. Upload the code to the device, then go to the website to see your data updating! **Note:** it may take up to a minute before the data appears the first time. You can check the status in the Pycom Console.

**Bonus:** Try setting up boolean, number and string assets in AllThingsTalk and see if you can send in other types of data. All assets must have different names, but they can be updated the same way in the code.

## 4. Read sensors
Now that the wifi is working, let's move on to reading data from a sensor. The main board includes both the soil moisture sensor and a DHT22 sensor which can sense temperature and humidity ([datasheet here](https://cdn-shop.adafruit.com/datasheets/Digital+humidity+and+temperature+sensor+AM2302.pdf)).

### Soil Moisture
1. Paste the following commands in the Pycom Console to read from the moisture sensor:

    ```python
    >>> from machine import Pin
    >>> from machine import ADC
    >>> moisture = ADC(Pin(32))
    >>> moisture.atten(ADC.ATTN_11DB)
    >>> print(moisture.read())
    ```
    If you send the last command several times, you will see different values depending on if you touch the sensor, or, say, put it in a plant. The value will be in the range 0 - 4095.

2. Replace the counter from the previous example with the soil moisture data. You will need to create a new asset in AllThingsTalk and add in the commands above in the right places.

    **Hint 1:** For some ideas on how to read the sensor, look in the folder `4-soil-moisture`.

    **Hint 2:** For a full working exampe, look in the folder `4-read-sensors`

**Bonus:** Add a graph in AllThingsTalk to show historical values.

### Temperature and Humidity
1. Paste the following commands in the Pycom Console to read from the DHT11 temperature and humidity sensor:

    ```python
    >>> from machine import Pin
    >>> from dht import DHT11
    >>> sensor = DHT11(Pin(22))
    >>> sensor.measure()
    >>> print("Temperature: {}  Humidity: {}".format(sensor.temperature(), sensor.humidity()))
    ```

    If you send the last command several times, you will see different values depending on if you breathe on the sensor, or, say, put it in a window that gets a lot of sun.

2. Create two new assets in AllThingsTalk for yout temperature and humidity data add in the commands above in the right places so that all three sensor values are sent to the cloud.

    **Hint 1:** For some ideas on how to read the sensor, look in the folder `4-temperature-humidity`.

    **Hint 2:** For a full working exampe, look in the folder `4-read-sensors`

**Bonus:** Add a temperature gauge in AllThingsTalk to show the current temperature.

## Choose your own adventure
You now have some options where to go next:
1. If you want to continue extending the hardware by connecting an additional light sensor, speaker and a display, continue to step 5, 6 and 7 respectively.

2. If you want to see what you can do with the data, you can play around with making dashboards in AllThingsTalk and setting it up in a way that suits your needs. You can for example set up a rule that sends you a notification when the moisture reaches a certain level. They also have an [API](https://docs.allthingstalk.com/developers/api/get-started/) that can be used to get the data into, for example, a Jupyter notebook if you are into that.

## 5. Light sensor

1. Disconnect the board from the computer and wire the light sensor like this:
  
    | Main board    | Light sensor  |
    | ------------- | ------------- |
    | 32            | V (VCC)       |
    | GND           | G (GND)       |
    | 35            | S (OUT)       |

    <img src=documentation/images/light-sensor.jpg width=600>
  
2. Paste the following commands in the Pycom Console to read from the sensor:

    ```python
    >>> from machine import Pin
    >>> from machine import ADC
    >>> light_sensor_power = Pin(32, Pin.OUT)
    >>> light_sensor = ADC(Pin(35))
    >>> light_sensor.atten(ADC.ATTN_11DB)
    >>> print(light_sensor.read())
    ```
    **Note:** In this example, the sensor gets power from GPIO pin 35. You could also use the `VCC` pin, but there is only one, and we will need it for the display in the next step! The light sensor draws very little current, so it is fine to power it from a pin like this.

3. Add the light sensor data to your device in AllThingsTalk.

  **Hint:** For some ideas on how to read the sensor, look in the folder `5-light-sensor`.

## 6. Write to the display
You now have sensing and connectivity in place. Now lets add some outputs and present your data on the LCD display. This kit includes a SD1306 0.96" 128x64 pixel LCD display that can be used to show custom graphics. Again, there is an example availabele.

1. Disconnect the USB cable and wire the SD1306 sensor like this:

    | Main board    | SD1306 display|
    | ------------- | ------------- |
    | VCC           | VDD           |
    | GND           | GND           |
    | 21            | SCK           |
    | 22            | SDA           |
    <img src=documentation/images/display.jpg width=600>

2. Add the folder `6-write-to-display` to your workspace in VSCode and remove any other workshop folders you have open.

3. Press upload and check that you see different graphics demos on the display.

4. Combine the example with your previous code by copying `ssd1306.py` into your folder, then look at the code in `main.py` to see how you can use it. The easiest way is to use `display.text()` to print your sensor values on four separate lines.

**Bonus:** Play around with the code and try to make it display the data in a way you like. How about a live moisture graph?

## 7. Play sound
There is also anouther type of output in the kit - a speaker! It can for example be used to notify the user if the moisture level gets too low.

1. Disconnect the USB cable and wire up the speaker module as follows. You will need to use the long cable that has a white connector in one end and connect to the board using three of the jumper wires. Sorry, the store did not have the right cable ¯\\\_(ツ)\_/¯

    | Main board    | Speaker module|
    | ------------- | ------------- |
    | 5V            | VDD           |
    | GND           | GND           |
    | 25            | SIG           |

    <img src=documentation/images/speaker.jpg width=600>

2. Add the folder `7-play-sound` to your workspace in VSCode and remove any other workshop folders you have open.

3. Press upload and check that you hear a sound demo play once.

4. Combine the example with your previous code by copying `speaker.py` into your folder, then look at the code in `main.py` to see how you can use it. One simple way would be to play a short tone every time the moisture sensor reads a value below a certain level.

**Bonus:** Play around with the code and try to make a good warning sound that is not too annoying to your future self (or your fellow workshop participants).

## 8. Combine Everything
That's it, you are now a certified IoT hardware maker! The final step of this workshop, if you have not done so already, is to combine all the examples so that the board can:

* Connect to AllThingsTalk
* Read soil moisture, temperature and humidity from the sensors
* Read ambient light level from the external sensor
* Display that data on the display
* Send that data to AllThingsTalk
* Play a sound if the plant needs attention

You can, for example, start by saving a copy of the counter example from step 3, then copy and paste code from the display example until you can see the sensor values on the display, then continue to also add in the other examples.

If you want some hints, there is also an example of how you might do this in `8-combine-everything`. Just put in your wifi settings, `device_id` and `device_token` in `config.py` like before and upload.

### Hints for further improvement
The provided example works fine in most cases, but does have some deliberate limitations for you to work on. For example;

* The display printout could look better.
* The code that sends data to AllThingsTalk does not check for errors.
* There also is no code for receiving data from cloud. You could for example set a threshold level in cloud and send it to the device.
