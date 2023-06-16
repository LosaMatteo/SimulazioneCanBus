import threading
import time
from Message import Message

'''
    Di seguito è riportato un esempio semplificato del protocollo di arbitraggio del CAN bus.
    Per rappresentare due nodi della rete che vogliono trasmettere un messaggio nel bus contemporaneamente, 
    abbiamo utilizzato dei thread che si contengono l'accesso ad una risorsa condivisa.
    Questa risorsa condivisa è rappresentata dal metodo send() che permette ad un thread (nodo) di completare la
    trasmissione del messaggio.
    Per permettere ad un nodo di leggere i messaggi trasmessi degli altri nodi, si è utilizzata la lista arbitration_id
    contenente gli id dei messaggi che devono essere trasmessi nel bus.
    Questa lista verrà passata come argomento al metodo arbitration() che contiene la logica dell'arbitraggio.
    In particolare, nel metodo compare(), viene mostrato il confronto bit a bit effettuato da un nodo tra l'id del
    messaggio trasmesso e quello ricevuto da un altro nodo, fermandosi quando un suo bit recessivo (1) viene sovrascritto
    da un bit dominante (0) e mettendosi in stato di attesa finché l'altro nodo non rilascia la risorsa condivisa.
    NOTA: Questo esempio semplificato, per ora, prevede l'esistenza di due soli nodi che vogliono trasmettere
    contemporaneamente.
'''

arbitration_id = []  # contiene gli arbitration id dei messaggi
sending = threading.Event()  # evento che garantisce la trasmissione esclusiva nel bus
rx_msg = []  # contiene i messaggi che sono stati inviati

# lower priority
msg0 = Message(
    id=0b111100,
    data=[1, 0, 0, 1, 3, 1, 4, 1], )

# higher priority
msg1 = Message(
    id=0b101100,
    data=[2, 1, 0, 1, 3, 1, 4, 1], )


def set_thread():
    thread0 = threading.Thread(target=transmit, args=(msg0, 0))
    thread1 = threading.Thread(target=transmit, args=(msg1, 1))
    thread0.start()
    thread1.start()


def send(msg, thread_id):
    time.sleep(1.0)
    sending.set()
    rx_msg.append(msg)
    arbitration_id.remove(bin(msg.id).replace('0b', ''))
    sending.clear()
    print(f"Thread #{thread_id} sent {bin(msg.id).replace('0b', '')}.\n")
    for i in rx_msg:
        time.sleep(1.5)
        if msg.data != i.data:
            print(f"Thread #{thread_id} received {i.data}.\n")


def transmit(msg, thread_id: int) -> None:
    print(f"Thread #{thread_id} wants to transmit.\n")
    arbitration_id.append(bin(msg.id).replace('0b', ''))
    time.sleep(1.0)
    while sending.is_set() or not arbitration(bin(msg.id).replace('0b', ''), arbitration_id, thread_id):
        sending.wait()
        print(f"Thread #{thread_id} is waiting...\n")
    send(msg, thread_id)


# le seguenti funzioni contengono la logica semplificata dell'arbitraggio
def arbitration(id, id_list: list, thread_id) -> bool:
    for i in id_list:
        if id != i:
            return compare(id, i, thread_id)
    return True


def compare(id1, id2, thread_id) -> bool:
    try:
        for char in range(0, len(id2)):
            print(f"Thread #{thread_id} is reading {id2[char]}.\n")
            if int(id1[char]) > int(id2[char]):
                print(f"Thread #{thread_id} stops transmission.\n")
                return False
        print(f"Thread #{thread_id} wins arbitration.\n")
        return True
    except:
        print(f"Thread #{thread_id} wins arbitration.\n")
        return True


if __name__ == "__main__":
    set_thread()
