import serial

def serial_connection(port, baudrate, timeout):
    arduino = serial.Serial(port, baudrate, timeout)
    if arduino.is_open is True:
        print("Arduino is successfully connected!")
    arduino.flushInput()
    return arduino


def read_serial_data(arduino):
    while True:
        serial_output = arduino.readline().decode('ascii')
        if serial_output:
            print(serial_output)
        else: #(elif serial_ouput == '':)
            break


def send_code(arduino, gcode):
    arduino.write(str.encode(f"{gcode}\n"))
#     while True:
#         line = arduino.readline()
#         print(line)
#         if line == b'ok\n':
#             break
    #arduino.write(b'\n')
    read_serial_data(arduino)