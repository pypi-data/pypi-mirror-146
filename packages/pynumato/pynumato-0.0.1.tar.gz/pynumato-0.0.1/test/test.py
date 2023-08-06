import pynumato.pynumato as pynumato
import time

delay=1
nb_run=5
port="COM27"
print("Run test ...")

for i in range(0,nb_run):
    print("Run ",i)
    numatoRelay= pynumato.Numato(numberRelays=2, port=port, baudrate=921600, timeout=delay)
    numatoRelay.get_version()

    numatoRelay.open_single_relay(0)
    time.sleep(delay)
    assert numatoRelay.get_single_relay(0)==1

    numatoRelay.close_single_relay(0)
    time.sleep(delay)
    assert numatoRelay.get_single_relay(0)==0

    numatoRelay.read_single_relay(1)
    numatoRelay.read_all_relays()

    numatoRelay.open_all_relays()
    time.sleep(delay)
    assert numatoRelay.get_single_relay(0)==1
    assert numatoRelay.get_single_relay(1)==1

    numatoRelay.close_all_relays()
    time.sleep(delay)
    assert numatoRelay.get_single_relay(0)==0
    assert numatoRelay.get_single_relay(1)==0

    numatoRelay.update_all_relays("oo")
    time.sleep(delay)
    assert numatoRelay.get_single_relay(0)==1
    assert numatoRelay.get_single_relay(1)==1

    numatoRelay.update_all_relays("cc")
    time.sleep(delay)
    assert numatoRelay.get_single_relay(0)==0
    assert numatoRelay.get_single_relay(1)==0

    numatoRelay.update_all_relays("oc")
    time.sleep(delay)
    assert numatoRelay.get_single_relay(0)==1
    assert numatoRelay.get_single_relay(1)==0

    numatoRelay.update_all_relays("co")
    time.sleep(delay)
    assert numatoRelay.get_single_relay(0)==0
    assert numatoRelay.get_single_relay(1)==1

    numatoRelay.update_all_relays("xx")
    time.sleep(delay)
    assert numatoRelay.get_single_relay(0)==0
    assert numatoRelay.get_single_relay(1)==1

# numatoRelay.reset()
# time.sleep(delay)
# print("get=",numatoRelay.get_single_relay(0))
# assert numatoRelay.get_single_relay(0)== 0
# print("get=",numatoRelay.get_single_relay(1))
# assert numatoRelay.get_single_relay(1)== 0

print("Run test Success")
