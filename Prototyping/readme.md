# Prototype User Manual

### 1. Download
Clone or download the repository

### 2. Capture Wireshark Data & Export to JSON
For the Prototype to be executed, there needs to be at least one wireshark capture.

The Prototype can only interpret probe requests so we recommend to use the capture filter
```
wlan.fc.type_subtype == 4 && ! _ws.malformed.expert
```
to filter all other wlan frames and malformed frames.

In Wireshark, klick "File > Export Packet Dissections > As JSON..." and save the file.

### 3. Save Location
Put the capture.JSON into the Prototype_Fingerprinting/Captures folder

### 4. Code Execution
Before the python program is executed, the file-path needs to be set to the capture file in the main.py

Example:
```
class Main:
    source_file = './Captures/{file_to_be_processed}.json'

    ...
```