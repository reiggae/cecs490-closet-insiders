import time

def read_card_id(ser):
    start_time = time.time()
    while time.time() - start_time < 10:
        if ser.in_waiting > 0:
            card_id = ser.readline().decode('ascii').strip()
            if card_id:
                return card_id
        time.sleep(0.1)
    return None