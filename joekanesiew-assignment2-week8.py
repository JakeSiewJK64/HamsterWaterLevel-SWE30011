import serial, time
import mysql.connector as mysql

# SERIAL CONFIGURATION
ser = serial.Serial('/dev/ttyS0',9600, timeout=1)
ser.reset_input_buffer()
WATERREADING = b"[WATERREADING]: "

# DATABASE CONFIGURATION
config = {
    'user':'JakeSiewJK64',
    'password':'welcome@123',
    'host':'localhost'
}

database = "JOEKANESIEW_SWE30011"
db = mysql.connect(**config)
cursor = db.cursor()
cursor.execute("USE {}".format(database))

def InitializeTables():
    cursor.execute("SHOW TABLES;")

    tables = [table[0] for table in cursor.fetchall()]
    print(tables)

    if "WaterReadings" not in tables:
        cursor.execute(
            """CREATE TABLE WaterReadings (
        readingId INTEGER (5) PRIMARY KEY NOT NULL AUTO_INCREMENT,
        readingValue INTEGER (3) NOT NULL,
        readingDate VARCHAR(255) NOT NULL
        );""")
        print("[AMIYA]: Created table WaterReadings.")

def InsertReadings(reading, time):
    cursor.execute(
            "INSERT INTO WaterReadings (readingValue, readingDate) VALUES ({},'{}');".format(int(reading), str(time))
            )
    db.commit()

def ProcessReadings(reading, time):
    cursor.execute("SELECT * FROM WaterReadings ORDER BY readingId DESC LIMIT 1;")
    data = [row[1] for row in cursor.fetchall()]
    if len(data) == 0:
        InsertReadings(reading, time)
    else:
        data = data[0]
        if reading != data:
            InsertReadings(reading, time)
            print("[AMIYA]: Stored Values for {} at {}".format(reading, time))

def MonitorReadings(reading):
    data = int(reading)
    if data <= 130:
        ser.write(b'1')
    else:
        ser.write(b'2')

if __name__ == '__main__':
    InitializeTables()
    while True:
        if ser.in_waiting > 0:
            reading = ser.readline()
            if WATERREADING in reading:
                try:
                    reading = reading[len(WATERREADING):len(reading)]
                    reading = reading.decode('utf-8').rstrip()
                    readTime = time.localtime()
                    readTime = time.strftime("%H:%M:%S (%m/%d/%Y)", readTime)
                    ProcessReadings(reading, readTime)
                    MonitorReadings(reading)
                except Exception as e:
                    print("error occured")
                    print(str(e))⏎