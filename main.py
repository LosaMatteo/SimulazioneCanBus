import threading
import time
from Message import Message

arbitration_id = []
choosing = threading.Event()
sending = threading.Event()
rx_msg = []

# lower priority
msg0 = Message(
    id=0b1111000000,
    data=[1, 0, 0, 1, 3, 1, 4, 1], )

# higher priority
msg1 = Message(
    id=0b101100,
    data=[2, 1, 0, 1, 3, 1, 4, 1], )


def _get_message(msg):
    return msg


def get_min_value(id_list):
    return min(id_list)


def set_thread():
    thread0 = threading.Thread(target=transmit, args=(msg0, 0))
    thread1 = threading.Thread(target=transmit, args=(msg1, 1))
    thread0.start()
    thread1.start()


def send(msg, thread_id):
    sending.set()
    print(f"Thread #{thread_id} is sending {bin(msg.id).replace('0b', '')}\n")
    rx_msg.append(msg)
    arbitration_id.remove(bin(msg.id).replace('0b', ''))
    sending.clear()
    print(f"Thread #{thread_id} sent {bin(msg.id).replace('0b', '')}\n")
    time.sleep(1.0)
    for i in rx_msg:
        print(i.id)


def transmit(msg, thread_id: int) -> None:
    print(f"Thread #{thread_id} wants to transmit.")
    arbitration_id.append(bin(msg.id).replace('0b', ''))
    if thread_id == 0:
        while not choosing.is_set():
            choosing.wait()
    else:
        choosing.set()

    while sending.is_set() or msg.id > get_min_value(arbitration_id):
        sending.wait()
        print(f"Thread #{thread_id} is waiting...\n")
    send(msg, thread_id)


if __name__ == "__main__":
    set_thread()

# with ProcessPoolExecutor() as executor:
#     executor.map(transmit, range(2))
