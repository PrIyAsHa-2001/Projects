#include <pgmspace.h>

#include <WiFiClientSecure.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include "WiFi.h"
#include <TinyGPS++.h>
#include <SoftwareSerial.h>


#define AWS_IOT_PUBLISH_TOPIC   "esp32/pub"
#define AWS_IOT_SUBSCRIBE_TOPIC "esp32/sub"


#define THINGNAME "My_esp32"                                       //change this

const char WIFI_SSID[] = "Lalith";                                        //change this
const char WIFI_PASSWORD[] = "9989862597";                                    //change this
const char AWS_IOT_ENDPOINT[] = "a1vfjjylz5cybm-ats.iot.us-west-2.amazonaws.com";        //change this

  int led = 22;     // LED pin
int button = 15; // push button is connected
int temp = 0;    // temporary variable for reading the button pin status








// Amazon Root CA 1
static const char AWS_CERT_CA[] PROGMEM = R"EOF(
-----BEGIN CERTIFICATE-----
MIIDQTCCAimgAwIBAgITBmyfz5m/jAo54vB4ikPmljZbyjANBgkqhkiG9w0BAQsF
ADA5MQswCQYDVQQGEwJVUzEPMA0GA1UEChMGQW1hem9uMRkwFwYDVQQDExBBbWF6
b24gUm9vdCBDQSAxMB4XDTE1MDUyNjAwMDAwMFoXDTM4MDExNzAwMDAwMFowOTEL
MAkGA1UEBhMCVVMxDzANBgNVBAoTBkFtYXpvbjEZMBcGA1UEAxMQQW1hem9uIFJv
b3QgQ0EgMTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBALJ4gHHKeNXj
ca9HgFB0fW7Y14h29Jlo91ghYPl0hAEvrAIthtOgQ3pOsqTQNroBvo3bSMgHFzZM
9O6II8c+6zf1tRn4SWiw3te5djgdYZ6k/oI2peVKVuRF4fn9tBb6dNqcmzU5L/qw
IFAGbHrQgLKm+a/sRxmPUDgH3KKHOVj4utWp+UhnMJbulHheb4mjUcAwhmahRWa6
VOujw5H5SNz/0egwLX0tdHA114gk957EWW67c4cX8jJGKLhD+rcdqsq08p8kDi1L
93FcXmn/6pUCyziKrlA4b9v7LWIbxcceVOF34GfID5yHI9Y/QCB/IIDEgEw+OyQm
jgSubJrIqg0CAwEAAaNCMEAwDwYDVR0TAQH/BAUwAwEB/zAOBgNVHQ8BAf8EBAMC
AYYwHQYDVR0OBBYEFIQYzIU07LwMlJQuCFmcx7IQTgoIMA0GCSqGSIb3DQEBCwUA
A4IBAQCY8jdaQZChGsV2USggNiMOruYou6r4lK5IpDB/G/wkjUu0yKGX9rbxenDI
U5PMCCjjmCXPI6T53iHTfIUJrU6adTrCC2qJeHZERxhlbI1Bjjt/msv0tadQ1wUs
N+gDS63pYaACbvXy8MWy7Vu33PqUXHeeE6V/Uq2V8viTO96LXFvKWlJbYK8U90vv
o/ufQJVtMVT8QtPHRh8jrdkPSHCa2XV4cdFyQzR1bldZwgJcJmApzyMZFo6IQ6XU
5MsI+yMRQ+hDKXJioaldXgjUkK642M4UwtBV8ob2xJNDd2ZhwLnoQdeXeGADbkpy
rqXRfboQnoZsG4q5WTP468SQvvG5M
-----END CERTIFICATE-----
)EOF";

// Device Certificate                                               //change this
static const char AWS_CERT_CRT[] PROGMEM = R"KEY(
-----BEGIN CERTIFICATE-----
MIIDWjCCAkKgAwIBAgIVAMwFWN0xggm7V0ne0SFheVhF+t65MA0GCSqGSIb3DQEB
CwUAME0xSzBJBgNVBAsMQkFtYXpvbiBXZWIgU2VydmljZXMgTz1BbWF6b24uY29t
IEluYy4gTD1TZWF0dGxlIFNUPVdhc2hpbmd0b24gQz1VUzAeFw0yMTExMDYxNDQ4
MzZaFw00OTEyMzEyMzU5NTlaMB4xHDAaBgNVBAMME0FXUyBJb1QgQ2VydGlmaWNh
dGUwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQC7Rd5d8KXcgmS8IPh3
vvpqkR4ZK3cxkTUYJvspb39+Bv73wW3LqAE3cTv+XWW0Qt9a7SrsggcVtwB97JOa
tHEzKukgD8Ek4jLtn1ro1EH4naih8YCt02ZONHx03dFOmCWcrMsOpkwyXk7aRY2s
mVBnVW1WSK2rjD8RF/XpxFXuGwy5NUUBoCVavnljwmtHZLePCuZ0yX+/H0sQwdzP
Pygck/r5XRhyd5WUbq5s/+OLRMMQ77WVD680H8t+pGvWSgj/ou7NdLlfyrOdvPm5
0xC+Z+vS+JZ7kctXErwdFiOFpJx92nK/uvffQqKLpTKWw1IPsvknsLza0TKjBL8b
X09xAgMBAAGjYDBeMB8GA1UdIwQYMBaAFKUaZ2BimfAOMnfqx4Jef3s1tmxpMB0G
A1UdDgQWBBSXwIckblY/pe3tIYFqsY8G9uOVHjAMBgNVHRMBAf8EAjAAMA4GA1Ud
DwEB/wQEAwIHgDANBgkqhkiG9w0BAQsFAAOCAQEAHEpuNts66sqdKgAwJQCRsUQw
s2kpYR4VmxMvQ22Jvtx8CkGdzC5TGyimNQCO6DOmAifohkhXuN33G7Piu87HtRNj
XtiWMyIPkdFnob5WhWsw5pTkWlnyS2hTTmi5CWtvmoCGDewZFCJQglkILdyPzAJK
Luw2Ldy3J9wCXgQDN7c+1MXWVy2AduPBSBQ1X8RLB4t3urIeiZXo48LWRcq5ms2I
Cj+nNqnl1lGvSAGgCiRLV/9L368Sty2GXr2hSi1XuXzXXgOrqSVfU5e9DIu+QA4Z
t3wzN2IpAx57ANsarL/U74188ym1qsE/n25PkxRnsa6QiM58T8Wmtn2iZYXbSw==
-----END CERTIFICATE-----
)KEY";

// Device Private Key                                               //change this
static const char AWS_CERT_PRIVATE[] PROGMEM = R"KEY(
-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEAu0XeXfCl3IJkvCD4d776apEeGSt3MZE1GCb7KW9/fgb+98Ft
y6gBN3E7/l1ltELfWu0q7IIHFbcAfeyTmrRxMyrpIA/BJOIy7Z9a6NRB+J2oofGA
rdNmTjR8dN3RTpglnKzLDqZMMl5O2kWNrJlQZ1VtVkitq4w/ERf16cRV7hsMuTVF
AaAlWr55Y8JrR2S3jwrmdMl/vx9LEMHczz8oHJP6+V0YcneVlG6ubP/ji0TDEO+1
lQ+vNB/LfqRr1koI/6LuzXS5X8qznbz5udMQvmfr0viWe5HLVxK8HRYjhaScfdpy
v7r330Kii6UylsNSD7L5J7C82tEyowS/G19PcQIDAQABAoIBAE0iBOmqQZZmOnlm
FxCzH08fQEdbqLdIuJafD5nMa7WLyh5flApqwz2DrRMigs5RMM+xmZlaIPLnshMr
iswQgAN0LBrhgkrfw9wtY3M8YYO15Av3fWmbBas2YQB9kEUP04YJgYUiJ4YjY9Tx
Ct5JM12sSOFeA/IBTMSMmuPS0xXDaAIsT0hC4F4ffuxtXP9TZNnyAZzyVhU7vlz1
MKsaW+/bJ5VqiPogRBl2Bhzu4CztziVwet0XNGtd/q6tiaacrfmufI7F0rnHkQ2a
Ttz1y9lI2zoI2mAUrhhFf7mz3DTLAFMvRmv972plMdpRx3gVbfsdcjwROp2ICQqf
bS+IYqUCgYEA3il2bQ1rPIhl4nENqLtFDrzXWgAucTnH9oPhxxhuAgeQIjPBWsbi
gK2/9SzLRSn72t7MzUhxTvheiDNCPlDC8W6252z7AhACRa7lucbmOyFdlY02fdsU
bsk1avTa0+OkU8zfPyHk0KHJZU0GrqhYUS+8dkNU8nvmTS+YGDZvxz8CgYEA18wD
Tcbo7Xpw0hc1AdsJK93xnthlbL0IUFx5Ob2nlvoUa6dc6mF4+BdrWCK6xJomkw5i
rK/z6o0fitDjCHKMFaMvBWbYVSWr5NJxRiiKhCe1NrrdePJJxGnKnV5BkkLC6/cP
16hhGT+JCYE85i+tjTaJq5ecMIFu1NkFfMk1bU8CgYA3KPROf1Zw4Szq3EcX7edn
kVum7QSa+E2912DnnhkyR85xr4gCkf8LFBjlNwoBUjtGTKttDN+VS/Wsu41nC4Zb
i7G+JEDuciseQh6n0cq4Q8CIsVcmSI76Mtsgg0sR8SOL6wJDGpdFdeYbUNSn6QSE
o+WXN4CP9FNqNrb8zAdU4QKBgQCSay92r1bOAvzX370slCTF6eKOZ79xp1UjyYrL
Pb6fdvEyFi26Lga5NpK0C2R0Dy/LKcCT8RLr+3MCajcRPT+FUuKNpLl2FIhsSslm
1A0gHB0dlG6/KI4awbkjS5fsGHZPSqQqLGotiml91H2wpXr5TJ7emZD1bGz56IKL
p64jiwKBgEgb7KnS4P2jersTdwFQC5RPDQjh4FzXKcRpm5abTk38QueAE1byaBif
TcXz2WuLvcy6fhqdqFCyffl/mSQt9Hd+vgOFwHMi6phE3YXjf2kRwZh9NkCfc7Um
6nSJFyjREn1NYAR+2fTG7RWeZanfUOxLDvD6PG8ItvTcqcggzaS1
-----END RSA PRIVATE KEY-----
)KEY";




WiFiClientSecure net = WiFiClientSecure();
PubSubClient client(net);

void connectAWS()
{
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

  Serial.println("Connecting to Wi-Fi");

  while (WiFi.status() != WL_CONNECTED){
    delay(500);
    Serial.print(".");
  }

  // Configure WiFiClientSecure to use the AWS IoT device credentials
  net.setCACert(AWS_CERT_CA);
  net.setCertificate(AWS_CERT_CRT);
  net.setPrivateKey(AWS_CERT_PRIVATE);

  // Connect to the MQTT broker on the AWS endpoint we defined earlier
  client.setServer(AWS_IOT_ENDPOINT, 8883);

  // Create a message handler
  client.setCallback(messageHandler);

  Serial.print("Connecting to AWS IOT");

  while (!client.connect(THINGNAME)) {
    Serial.print(".");
    delay(100);
  }

  if(!client.connected()){
    Serial.println("AWS IoT Timeout!");
    return;
  }

  // Subscribe to a topic
  client.subscribe(AWS_IOT_SUBSCRIBE_TOPIC);

  Serial.println("AWS IoT Connected!");
}

/*void publishMessage()
{
StaticJsonDocument<200> doc;
  
 doc["Button_status"] = digitalRead(button);
char jsonBuffer[512];
serializeJson(doc, jsonBuffer); // print to client

  client.publish(AWS_IOT_PUBLISH_TOPIC, jsonBuffer);
}
*/
void publishMessage()
{
  char payload[512];
  sprintf(payload,"{\"Action\":\"pressed\"}");
  client.publish(AWS_IOT_PUBLISH_TOPIC, payload);
  Serial.print("Published Message:");
  Serial.println(payload);
}

void messageHandler(char* topic, byte* payload, unsigned int length) {
  Serial.print("incoming: ");
  Serial.println(topic);

  StaticJsonDocument<200> doc;
  deserializeJson(doc, payload);
  const char* message = doc["message"];
  Serial.println(message);
}



void setup() {
  Serial.begin(9600);
  connectAWS();
  pinMode(led, OUTPUT);   // declare LED as output
  pinMode(button, INPUT);// declare push button as input
  
}


   
  
 

void loop() {
  temp = digitalRead(button);
    // This sketch displays information every time a new sentence is correctly encoded.
 
     
     if (temp == HIGH) {
        digitalWrite(led, HIGH);
        Serial.println("LED Turned ON");
        
        publishMessage();
         client.loop();
        delay(1000);
       }
   else {
        digitalWrite(led, LOW);
       
         client.loop();
        delay(1000);
       }

 
 
 
}
