from tkinter import Label, ttk, StringVar, Button, IntVar, Entry, END
from datetime import datetime
from time import sleep
from pyfirmata2 import Arduino
from datetime import datetime

class SensorGUI:
    # class for creating a ski weather summary GUI
    def __init__(self, master, pinsInfo, inputVoltage=5, readingFrequency=500):
        self._master = master
        self._master.geometry("600x350")
        self._set_current_time_in_title()
        
        #fonts
        boldFont = ("Helvetica", 10, "bold")
        regularFont = ("Helvetica", 10)
        
        self._inputVoltage = inputVoltage
        self._readingFrequency = readingFrequency
        
        rowCount = 0
        self._pins = []
        self._entries = []
        self._sensorTypes = []
        for pinInfo in pinsInfo:
            pin, pinTitle, sensorType = pinInfo
            
            self._pins.append(pin)
            self._sensorTypes.append(sensorType)
            
            pinLabel = Label(master, text=pinTitle, font=regularFont)
            pinLabel.grid(row=rowCount, column=0, sticky="w")
            
            pinEntry = Entry(master)
            pinEntry.grid(row=rowCount, column=1, sticky="w")
            self._entries.append(pinEntry)
            
            rowCount += 1
        
        self._set_current_time_in_title()
        self._update_pins()
            
    def _update_pins(self):
        for index, pin in enumerate(self._pins):
            sensorReading = "None"
            analogReading = pin.read()
            if analogReading:
                voltage = self._convert_from_analog_input_to_voltage(analogReading)
                
                if self._sensorTypes[index] == "Temperature":
                    sensorReading = f"{self._get_temperature_from_voltage(voltage):.2f}"
                else:
                    sensorReading = f"{voltage:.2f}"
                
            self._entries[index].delete(0, END) # deletes the current value
            self._entries[index].insert(0, sensorReading) # inserts the new value
        self._master.after(self._readingFrequency, self._update_pins)
            
        
    def _update_temperature(self):
        tempValue = "None"
        tempReading = self._tempPin.read()
        if tempReading:
            tempValue = f"{self._get_temperature_from_analog_input(tempReading):.2f}"
        self._temperatureEntry.delete(0, END) #deletes the current value
        self._temperatureEntry.insert(0, tempValue) # inserts the new value
        self._temperatureEntry.after(self._readingFrequency, self._update_temperature)
        
    def _update_noise(self):
        noiseValue = "None"
        noiseReading = self._noisePin.read()
        if noiseReading:
            noiseValue = f"{self._get_noise_from_analog_input(noiseReading):.2f}"
        self._noiseEntry.delete(0, END) #deletes the current value
        self._noiseEntry.insert(0, noiseValue) # inserts the new value
        self._noiseEntry.after(self._readingFrequency, self._update_noise)
        
    def _update_light_front(self):
        lightValue = "None"
        lightReading = self._lightFrontPin.read()
        if lightReading:
            lightValue = f"{self._get_light_from_analog_input(lightReading):.2f}"
        self._lightEntryFront.delete(0, END) #deletes the current value
        self._lightEntryFront.insert(0, lightValue) # inserts the new value
        self._lightEntryFront.after(self._readingFrequency, self._update_light_front)    
    
    def _update_light_back(self):
        lightValue = "None"
        lightReading = self._lightBackPin.read()
        if lightReading:
            lightValue = f"{self._get_light_from_analog_input(lightReading):.2f}"
        self._lightEntryBack.delete(0, END) #deletes the current value
        self._lightEntryBack.insert(0, lightValue) # inserts the new value
        self._lightEntryBack.after(self._readingFrequency, self._update_light_back) 
        
    def _set_current_time_in_title(self):
        timeNow = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        self._master.title("Sensor data " + timeNow)
        self._master.after(1000, self._set_current_time_in_title)
        
    def _convert_from_analog_input_to_voltage(self, analogValue):
        return analogValue * self._inputVoltage
        
    def _get_temperature_from_voltage(self, voltage):
        
        return (voltage - 0.5) * 100
        
    def _get_noise_from_analog_input(self, analogValue):
        voltage = (self._convert_from_analog_input_to_voltage(analogValue))
        
        return voltage
        
    def _get_light_from_analog_input(self, analogValue):
        voltage = (self._convert_from_analog_input_to_voltage(analogValue))
        
        return voltage
        
    
        

    