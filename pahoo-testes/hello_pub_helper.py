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

# Execution
while True:
    temperature = input("Enter temperature: ")
    
    if(type(temperature) is str and 
        temperature.lower().startswith('s')):
            break
     publish.single(topic="paho/test/single", 
                    payload=temperature, 
                    hostname="localhost")

    
