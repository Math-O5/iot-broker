import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import signal
import sys

# Quando conectar-se ao servidor
def on_connect(client, userdata, flags, rc):
    print("Connected with client, code: " + str(rc))
    
    client.subscribe("$SYS/#")

# Quando receber uma mensagem
def on_message(client, message, msg, rest):
    print("Ué: " + str(rest))
    """
        msg : {
            topic,
            payload
        }
    """
    print("Msg:")
    print(msg)
    # print(msg.topic+" "+str(msg.payload))

def on_subscribe(client, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_publish(client, obj, mid):
    print("mid: " + str(mid))

# Terminar execução: CTRL+C
def exit_broke(signum, frame):
    # Restaurar orginal signal handler quando CRTL+C é pressionado
    signal.signal(signal.SIGINT, original_sigint)

    try:
        if input("\nDeseja terminar o programa? (y/n)> ").lower().startswith('y'):
            sys.exit(1)

    except KeyboardInterrupt:
        print("Ok")
        sys.exit(1)

    # restore the exit gracefully handler here    
    signal.signal(signal.SIGINT, exit_gracefully)


# Alterar signal para permitir terminar programa com CTRL+C
original_sigint = signal.getsignal(signal.SIGINT)
signal.signal(signal.SIGINT, exit_broke)

# Start Connection
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish
client.on_subscribe = on_subscribe

client.connect("127.0.0.1", 1884, 60)
client.loop_start()

# Execution
while True:
    temperature = input("Enter temperature: ")
    
    if(type(temperature) is str and 
        temperature.lower().startswith('s')):
            client.loop_stop()
            break
    client.publish(topic="paho/test/data", 
                    payload=temperature, qos=0)

    