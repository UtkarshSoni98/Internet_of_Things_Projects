import conf
from boltiot import Sms, Bolt
import  json , time , datetime
from pyfiglet import Figlet
import pyttsx3;
engine = pyttsx3.init();
f= Figlet(font='slant',width=200)
print(f.renderText('Hello , Welcome To Temperature Monitoring System'))
engine.setProperty('rate', 160)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.say("Hello, Everyone, Welcome To Temperature Monitoring System");
engine.runAndWait() ;
engine.say('Please Wait for a while, We are fetching our data');
engine.runAndWait() ;
time.sleep(2)

minimum_limit = 400  #39.06 Degree Celsius
maximum_limit = 600  #58.59 Degree Celsius
mybolt = Bolt(conf.API_KEY, conf.DEVICE_ID)
sms = Sms(conf.SSID, conf.AUTH_TOKEN, conf.TO_NUMBER, conf.FROM_NUMBER)

while True:
    fb = open("TempData1.txt", "a")
    fa = open("DangerTemp1.txt", "a")
    resp = mybolt.analogRead('A0')
    data = json.loads(resp)
    try:
        sensor_value = int(data['value'])
        Temperature = (100 * sensor_value) / 1024

        Temp=round(Temperature,2)
        print(f"  Room Temperature at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} is : {Temp} Degree Celsius")
        engine.say(f"  Room Temperature at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} is : {Temp} Degree Celsius")
        engine.runAndWait();
        fb.write(f"  Room Temperature at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} is : {Temp} Degree Celsius \n")

        if sensor_value > maximum_limit or sensor_value < minimum_limit:
            response = sms.send_sms(f"The Current temperature is {str(Temp)} Degree Celsius at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ") #mailer.send_email("Alert", "The Current temperature sensor value is " +str(Temp))
            fa.write(f" Critical Room Temperature at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} is : {Temp} Degree Celsius \n")
            engine.say("Oops, Critical Alert,  Temperature Crossed the limit , Please Maintain the Temperature ");
            engine.runAndWait();
            engine.say("We Are Sending Alert sms to the Registered Mobile number ");
            engine.runAndWait();
    except Exception as e:
        print('Error',e)
    engine.say("Next Alert is coming in 20 seconds");
    engine.runAndWait();
    fa.close()
    fb.close()
    time.sleep(20)
