from tkinter import Label, ttk, StringVar, Button, IntVar, Entry, END
from datetime import datetime
from time import sleep
from pyfirmata2 import Arduino
from datetime import datetime

class SensorGUI:
    # class for creating a ski weather summary GUI
    def __init__(self, master, temperaturePin, noisePin, lightPin, inputVoltage=5, updateReadingFrequency=500):
        self._master = master
        self._master.geometry("600x350")
        self._set_current_time_in_title()
        
        #fonts
        boldFont = ("Helvetica", 10, "bold")
        regularFont = ("Helvetica", 10)
        
        self._inputVoltage = inputVoltage
        self._updateReadingFrequency = updateReadingFrequency
        
        self._tempPin = temperaturePin
        self._noisePin = noisePin
        self._lightPin = lightPin
        
        temperatureLabel = Label(master, text="Temperature", font=regularFont)
        temperatureLabel.grid(row=0, column=0, sticky="w")
        
        self._temperatureEntry = Entry(master)
        self._temperatureEntry.grid(row=0, column=1)
        self._update_temperature()
        
        noiseLabel = Label(master, text="Noise", font=regularFont)
        noiseLabel.grid(row=1, column=0, sticky="w")
        
        self._noiseEntry = Entry(master)
        self._noiseEntry.grid(row=1, column=1)
        self._update_noise()
        
        lightLabel = Label(master, text="Light", font=regularFont)
        lightLabel.grid(row=2, column=0, sticky="w")
        
        self._lightEntry = Entry(master)
        self._lightEntry.grid(row=2, column=1)
        self._update_light()
        
    def _update_temperature(self):
        tempValue = "None"
        tempReading = self._tempPin.read()
        if tempReading:
            tempValue = f"{self._get_temperature_from_analog_input(tempReading):.2f}"
        self._temperatureEntry.delete(0, END) #deletes the current value
        self._temperatureEntry.insert(0, tempValue) # inserts the new value
        self._temperatureEntry.after(self._updateReadingFrequency, self._update_temperature)
        
    def _update_noise(self):
        noiseValue = "None"
        noiseReading = self._noisePin.read()
        if noiseReading:
            noiseValue = f"{self._get_noise_from_analog_input(noiseReading):.2f}"
        self._noiseEntry.delete(0, END) #deletes the current value
        self._noiseEntry.insert(0, noiseValue) # inserts the new value
        self._noiseEntry.after(self._updateReadingFrequency, self._update_noise)
        
    def _update_light(self):
        lightValue = "None"
        lightReading = self._lightPin.read()
        if lightReading:
            lightValue = f"{self._get_light_from_analog_input(lightReading):.2f}"
        self._lightEntry.delete(0, END) #deletes the current value
        self._lightEntry.insert(0, lightValue) # inserts the new value
        self._lightEntry.after(self._updateReadingFrequency, self._update_light)    
    
        
    def _set_current_time_in_title(self):
        timeNow = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        self._master.title("Sensor data " + timeNow)
        self._master.after(1000, self._set_current_time_in_title)
        
    def _convert_from_analog_input_to_voltage(self, analogValue):
        return analogValue * self._inputVoltage
        
    def _get_temperature_from_analog_input(self, analogValue):
        voltage = self._convert_from_analog_input_to_voltage(analogValue)
        
        return (voltage - 0.5) * 100
        
    def _get_noise_from_analog_input(self, analogValue):
        voltage = (self._convert_from_analog_input_to_voltage(analogValue))
        
        return voltage
        
    def _get_light_from_analog_input(self, analogValue):
        voltage = (self._convert_from_analog_input_to_voltage(analogValue))
        
        return voltage
        
    
        
        """
        # input widgets
        whereLabel = Label(master, text="Where do you want to ski?", font=regularFont)
        whereLabel.grid(row=0, column=0, sticky="w", columnspan=2, pady=1, ipadx=3)
        
        self._places = StringVar()
        self._placesChosen = ttk.Combobox(master, width=15, textvariable=self._places)
        self._placesChosen["values"] = list(self._placesUrls.keys())
        self._placesChosen.grid(row=1, column=0, pady=5, sticky="w", columnspan=2, padx=3)
        self._placesChosen.current(0)

        timeLabel = Label(master, text="When do you want to ski?", font=regularFont)
        timeLabel.grid(row=2, column=0, sticky="w", columnspan=2, pady=1, ipadx=3)

        dateLabel = Label(master, text="Date", font=regularFont)
        dateLabel.grid(row=3, column=0)

        fromHourLabel = Label(master, text="From (hour)", font=regularFont)
        fromHourLabel.grid(row=3, column=1)

        durationLabel = Label(master, text="Duration (hours)", font=regularFont)
        durationLabel.grid(row=3, column=2)

        self._day = StringVar()
        self._dayChosen = ttk.Combobox(master, width=10, textvariable= self._day)
        self._dayChosen["values"] = self._getDates()
        self._dayChosen.grid(row=4, column=0, padx=3, pady=5, sticky="w")
        self._dayChosen.current(0)

        self._hour = StringVar()
        self._hourChosen = ttk.Combobox(master, width=10, textvariable= self._hour)
        self._hourChosen.grid(row=4, column=1, padx=10, sticky="w")
        self._getHours()

        self._dayChosen.bind("<<ComboboxSelected>>", self._setHours)

        self._duration = IntVar()
        self._durationChosen = ttk.Combobox(master, width=10, textvariable=self._duration)
        self._durationChosen['values'] = [x for x in range(1, 31)]
        self._durationChosen.grid(row=4, column=2)
        self._durationChosen.current(3)

        execute = Button(master, bg="cyan", text="Check", command=self._addWeatherAndLubricationInfo)
        execute.grid(row=5, column=1)
        
        # output widgets
        self._descTitleLabel = Label(master, text="Weather", font=boldFont)
        self._descTitleLabel.grid(row=6, column=0, sticky="w", ipadx=3, pady=2)

        self._descLabel = Label(master, font=regularFont)
        self._descLabel.grid(row=6, column=1, columnspan=8, sticky="w")
        
        self._temperatureTitleLabel = Label(master, text = "Temperature", font=boldFont)
        self._temperatureTitleLabel.grid(row=7, column=0, sticky="w", ipadx=3, pady=2)

        self._temperatureLabel = Label(master, font=regularFont)
        self._temperatureLabel.grid(row=7, column=1, columnspan=8, sticky="w")
        
        self._windTitleLabel = Label(master, text="Winds", font=boldFont)
        self._windTitleLabel.grid(row=8, column=0, sticky="w", ipadx=3, pady=2)
        
        self._windLabel = Label(master, font=regularFont)
        self._windLabel.grid(row=8, column=1, columnspan=8, sticky="w")

        self._precipitationTitleLabel = Label(master, text="Precipitation", font=boldFont)
        self._precipitationTitleLabel.grid(row=9, column=0, rowspan=3, sticky="nw", ipadx=3, pady=2)

        self._precipitationLabel = Label(master, justify="left", font=regularFont)
        self._precipitationLabel.grid(row=9, column=1, columnspan=8, sticky="w")
        
        self._lubricationTitleLabel = Label(master, text="Lubrication", font=boldFont)
        self._lubricationTitleLabel.grid(row=10, column=0, sticky="w", ipadx=3, pady=2)

        self._lubricationLabel = Label(master, font=regularFont)
        self._lubricationLabel.grid(row=10, column=1, columnspan=9, sticky="w")
        
        self._snowDepthTitleLabel = Label(master, text="Snow depth", font=boldFont)
        self._snowDepthTitleLabel.grid(row=11, column=0, sticky="w", ipadx=3, pady=2)
        
        self._snowDepthLabel = Label(master, font=regularFont)
        self._snowDepthLabel.grid(row=11, column=1, columnspan=8, sticky="w")
        """
    