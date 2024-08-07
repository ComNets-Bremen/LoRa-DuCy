from network import LoRa
import socket
import time
import pycom
from machine import Timer
import crypto
from network import WLAN
from network import Bluetooth
import machine
import ustruct, ubinascii, uhashlib

from lib.varlogger import VarLogger as vl
import _thread
import gc
import sys
import utime

'''
Implemented of LoPy4/Fipy with 1.18 pycom-micropython version
'''
######### Utility Functions #######################
def get_node_id(hex=False):
    """
    Get node id, which consists of four bytes unsigned int.
    Return as hex, according to parameter.
    """
    _fun_name = 'get_node_id'
    _cls_name = '0'
    _thread_id = _thread.get_ident()

    node_id = ubinascii.hexlify(uhashlib.sha1(
        machine.unique_id()).digest()).decode("utf-8")[-8:]
    vl.log(var='node_id', fun=_fun_name, clas=_cls_name, th=_thread_id)

    if hex:
        return node_id
    else:
        return int(node_id, 16)


gc.collect()
################################## Start of the main code ##################################
_thread_id = _thread.get_ident()
_fun_name = '0'
_cls_name = '0'

vl.thread_status(_thread_id, 'active')     #### MUST


######### Initialize the device #######################
lora = LoRa(mode=LoRa.LORA, power_mode=LoRa.ALWAYS_ON, region=LoRa.EU868)
vl.log(var='lora', fun=_fun_name, clas=_cls_name, th=_thread_id)
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
vl.log(var='s', fun=_fun_name, clas=_cls_name, th=_thread_id)
s.setblocking(False)
pycom.heartbeat(False)
wlan = WLAN()
vl.log(var='wlan', fun=_fun_name, clas=_cls_name, th=_thread_id)
wlan.deinit()
bluetooth = Bluetooth()
vl.log(var='bluetooth', fun=_fun_name, clas=_cls_name, th=_thread_id)
bluetooth.deinit()



######### Own node's information #####################
if get_node_id() == 235968217:
    my_number = 1
    vl.log(var='my_number', fun=_fun_name, clas=_cls_name, th=_thread_id)
    source_address = 'Mac' + str(my_number)
    vl.log(var='source_address', fun=_fun_name, clas=_cls_name, th=_thread_id)
    print('I am node Mac1')
elif get_node_id() == 829745241:
    my_number = 2
    vl.log(var='my_number', fun=_fun_name, clas=_cls_name, th=_thread_id)
    source_address = 'Mac' + str(my_number)
    vl.log(var='source_address', fun=_fun_name, clas=_cls_name, th=_thread_id)
    print('I am node Mac2')
elif get_node_id() == 50989579:
    my_number = 3
    vl.log(var='my_number', fun=_fun_name, clas=_cls_name, th=_thread_id)
    source_address = 'Mac' + str(my_number)
    vl.log(var='source_address', fun=_fun_name, clas=_cls_name, th=_thread_id)
    print('I am node Mac3')

number_of_neighbours = 2
vl.log(var='number_of_neighbours', fun=_fun_name, clas=_cls_name, th=_thread_id)


######### Initialize the timers #######################
chrono = Timer.Chrono()
vl.log(var='chrono', fun=_fun_name, clas=_cls_name, th=_thread_id)
chrono1 = Timer.Chrono()
vl.log(var='chrono1', fun=_fun_name, clas=_cls_name, th=_thread_id)
chrono2 = Timer.Chrono()
vl.log(var='chrono2', fun=_fun_name, clas=_cls_name, th=_thread_id)
chrono3 = Timer.Chrono()
vl.log(var='chrono3', fun=_fun_name, clas=_cls_name, th=_thread_id)

############ Configurable Parameters #################
wakeup_interval = 20
vl.log(var='wakeup_interval', fun=_fun_name, clas=_cls_name, th=_thread_id)
fast_sleep_threshold = 2.5
vl.log(var='fast_sleep_threshold', fun=_fun_name, clas=_cls_name, th=_thread_id)
transmission_type = 'Unicast'  #Unicast or Broadcast
vl.log(var='transmission_type', fun=_fun_name, clas=_cls_name, th=_thread_id)
num_of_packets = 10
vl.log(var='num_of_packets', fun=_fun_name, clas=_cls_name, th=_thread_id)
pll_threshold = 7
vl.log(var='pll_threshold', fun=_fun_name, clas=_cls_name, th=_thread_id)
cca_duration = 0.08
vl.log(var='cca_duration', fun=_fun_name, clas=_cls_name, th=_thread_id)
cca_interval = 0.4
vl.log(var='cca_interval', fun=_fun_name, clas=_cls_name, th=_thread_id)
rssi_threshold = 100
vl.log(var='rssi_threshold', fun=_fun_name, clas=_cls_name, th=_thread_id)
packet_size = 255  # bytes
vl.log(var='packet_size', fun=_fun_name, clas=_cls_name, th=_thread_id)

############ Configuring the device ####################
packet_number = 1
vl.log(var='packet_number', fun=_fun_name, clas=_cls_name, th=_thread_id)
transmissions = 0
vl.log(var='transmissions', fun=_fun_name, clas=_cls_name, th=_thread_id)
alive_time = 0
vl.log(var='alive_time', fun=_fun_name, clas=_cls_name, th=_thread_id)
phase_lock_time_saving = 0
vl.log(var='phase_lock_time_saving', fun=_fun_name, clas=_cls_name, th=_thread_id)
saved_transmissions = 0
vl.log(var='saved_transmissions', fun=_fun_name, clas=_cls_name, th=_thread_id)
failed_attempts = 0
vl.log(var='failed_attempts', fun=_fun_name, clas=_cls_name, th=_thread_id)
phase_lock_cca_fails = 0
vl.log(var='phase_lock_cca_fails', fun=_fun_name, clas=_cls_name, th=_thread_id)
Awake_instance = 1
vl.log(var='Awake_instance', fun=_fun_name, clas=_cls_name, th=_thread_id)
broadcast_time_save = 0
vl.log(var='broadcast_time_save', fun=_fun_name, clas=_cls_name, th=_thread_id)
fast_sleep_time_save = 0
vl.log(var='fast_sleep_time_save', fun=_fun_name, clas=_cls_name, th=_thread_id)
Full_send_time = 0
vl.log(var='Full_send_time', fun=_fun_name, clas=_cls_name, th=_thread_id)
Tx_time = 0
vl.log(var='Tx_time', fun=_fun_name, clas=_cls_name, th=_thread_id)
Rx_time = 0
vl.log(var='Rx_time', fun=_fun_name, clas=_cls_name, th=_thread_id)
ack = False
vl.log(var='ack', fun=_fun_name, clas=_cls_name, th=_thread_id)
only_listen = False
vl.log(var='only_listen', fun=_fun_name, clas=_cls_name, th=_thread_id)
noise_detected_counter = 0
vl.log(var='noise_detected_counter', fun=_fun_name, clas=_cls_name, th=_thread_id)
ack_data_packets = []
vl.log(var='ack_data_packets', fun=_fun_name, clas=_cls_name, th=_thread_id)
cca_list = []
vl.log(var='cca_list', fun=_fun_name, clas=_cls_name, th=_thread_id)
received_time = []
vl.log(var='received_time', fun=_fun_name, clas=_cls_name, th=_thread_id)
received_full_data = []
vl.log(var='received_full_data', fun=_fun_name, clas=_cls_name, th=_thread_id)
phase_lock_optimization = {}
vl.log(var='phase_lock_optimization', fun=_fun_name, clas=_cls_name, th=_thread_id)
phase_lock_optimization_time = {}
vl.log(var='phase_lock_optimization_time', fun=_fun_name, clas=_cls_name, th=_thread_id)
max_wait_time = 1 * wakeup_interval
vl.log(var='max_wait_time', fun=_fun_name, clas=_cls_name, th=_thread_id)
lora_off_time = 0.6
vl.log(var='lora_off_time', fun=_fun_name, clas=_cls_name, th=_thread_id)
packet_gap_interval = 1
vl.log(var='packet_gap_interval', fun=_fun_name, clas=_cls_name, th=_thread_id)
pll_activation = 2.0
vl.log(var='pll_activation', fun=_fun_name, clas=_cls_name, th=_thread_id)
sleep_in_pll = 1.9
vl.log(var='sleep_in_pll', fun=_fun_name, clas=_cls_name, th=_thread_id)
transmission_in_pll = 1.8
vl.log(var='transmission_in_pll', fun=_fun_name, clas=_cls_name, th=_thread_id)

############## Delay to avoid CCA overlap ############
number2 = (wakeup_interval - 2) / 10
vl.log(var='number2', fun=_fun_name, clas=_cls_name, th=_thread_id)
print((my_number - 1) * number2)
time.sleep((my_number - 1) * number2)



############## Random number generation ################
def Random():
    _fun_name = 'Random'
    _cls_name = '0'
    _thread_id = _thread.get_ident()

    r = crypto.getrandbits(32)
    vl.log(var='r', fun=_fun_name, clas=_cls_name, th=_thread_id)
    return ((r[0] << 24) + (r[1] << 16) + (r[2] << 8) + r[3]) / 4294967295.0

def RandomRange(rfrom, rto):
    _fun_name = 'RandomRange'
    _cls_name = '0'
    _thread_id = _thread.get_ident()

    vl.log(var='0', fun=_fun_name, clas=_cls_name, th=_thread_id)
    return Random() * (rto - rfrom) + rfrom

############## Random packet generation ################
def packet_check(packet_status, s=Awake_instance, g=packet_number):
    _fun_name = 'packet_check'
    _cls_name = '0'
    _thread_id = _thread.get_ident()

    if not packet_status:
        total_nodes = number_of_neighbours+1
        number = (Awake_instance % total_nodes) - my_number
        vl.log(var='number', fun=_fun_name, clas=_cls_name, th=_thread_id)

        if packet_number < num_of_packets and (number == 0 or number == -total_nodes):
            return True
        else:
            return False
    else:
        return packet_status



############## Clear Channel Assessment ################
def cca(x=packet_gap_interval, f=lora_off_time, c=cca_list, d=chrono, l=lora, h=cca_duration, m=rssi_threshold, n=cca_interval):
    _fun_name = 'cca'
    _cls_name = '0'
    _thread_id = _thread.get_ident()

    print('Checking Channel')
    chrono1.start()
    while chrono1.read() < cca_duration:
        c.append(str(lora.ischannel_free(-rssi_threshold)))
        # print('RSSI during CCA {}'.format (lora.stats()[1]))
        vl.log(var='c', fun=_fun_name, clas=_cls_name, th=_thread_id)
    chrono1.stop()
    chrono1.reset()
    chrono.stop()
    # print('cca list', c)

    if 'False' in cca_list:
        return False
    else:
        chrono1.start()
        while chrono1.read() < cca_interval:
            l = LoRa(power_mode=LoRa.SLEEP, region=LoRa.EU868)
            vl.log(var='l', fun=_fun_name, clas=_cls_name, th=_thread_id)
        l = LoRa(power_mode=LoRa.ALWAYS_ON, region=LoRa.EU868)
        vl.log(var='l', fun=_fun_name, clas=_cls_name, th=_thread_id)
        chrono1.stop()
        chrono1.reset()
        chrono.start()
        chrono1.start()

        while chrono1.read() < cca_duration:
            c.append(str(lora.ischannel_free(-rssi_threshold)))
            # print('RSSI during CCA {}'.format (lora.stats()[1]))
            vl.log(var='c', fun=_fun_name, clas=_cls_name, th=_thread_id)
        chrono1.stop()
        chrono1.reset()

        if 'False' in cca_list:
            return False
        else:
            return True



############# Neighbor Discovery #########################
neighbour_discover = False
vl.log(var='neighbour_discover', fun=_fun_name, clas=_cls_name, th=_thread_id)
neighbor_adresses = []
vl.log(var='neighbor_adresses', fun=_fun_name, clas=_cls_name, th=_thread_id)
while not neighbour_discover:
    print('Discovering Neighbours')
    number = int(RandomRange(1, 4))
    print(number, my_number)
    vl.log(var='number', fun=_fun_name, clas=_cls_name, th=_thread_id)
    if number != my_number:
        neighbor = 'Mac' + str(number)
        vl.log(var='neighbor', fun=_fun_name, clas=_cls_name, th=_thread_id)
        print('Neighbor Mac{} added to the list'.format(neighbor))
        if neighbor not in neighbor_adresses:
            neighbor_adresses.append(neighbor)
            vl.log(var='neighbor_adresses', fun=_fun_name, clas=_cls_name, th=_thread_id)
            if len(neighbor_adresses) == number_of_neighbours:
                break
    # time.sleep(1)

print('Neighbour Addresses:', neighbor_adresses)
Broadcast_address = 'All'
vl.log(var='Broadcast_address', fun=_fun_name, clas=_cls_name, th=_thread_id)
neighbor = 0
vl.log(var='neighbor', fun=_fun_name, clas=_cls_name, th=_thread_id)

###### for testing purposes ######
gc_start_time = utime.ticks_ms()
gc.collect()
print('gc.collect duration:', utime.ticks_ms()-gc_start_time)
###### for testing purposes ######

##### for testing purposes ######
testing_start = vl.created_timestamp
##### for testing purposes ######

print('Initialising Contiki MAC')
packet_status = False
vl.log(var='packet_status', fun=_fun_name, clas=_cls_name, th=_thread_id)

############# Contiki MAC #########################
while True:
    try:

        ##### for testing purposes ######
        print('Time since started:', utime.ticks_ms()- testing_start - vl.time_to_write )
        ##### for testing purposes ######

        chrono.start()
        chrono3.start()
        channel_status = cca(chrono, cca_list)
        vl.log(var='channel_status', fun=_fun_name, clas=_cls_name, th=_thread_id)
        packet_status = packet_check(packet_status, Awake_instance, packet_number)
        vl.log(var='packet_status', fun=_fun_name, clas=_cls_name, th=_thread_id)
        lora = LoRa(power_mode=LoRa.ALWAYS_ON, region=LoRa.EU868)
        vl.log(var='lora', fun=_fun_name, clas=_cls_name, th=_thread_id)

        while len(s.recv(packet_size)) > 0:
            ss = s.recv(packet_size)
            vl.log(var='ss', fun=_fun_name, clas=_cls_name, th=_thread_id)
            events = lora.events()
            vl.log(var='events', fun=_fun_name, clas=_cls_name, th=_thread_id)

        print('Channel Status:', channel_status)
        print('Packet Status:', packet_status)
        if channel_status and packet_status and not only_listen:
            ########### Transmit Data ##########################
            lora = LoRa(power_mode=LoRa.ALWAYS_ON, region=LoRa.EU868)
            vl.log(var='lora', fun=_fun_name, clas=_cls_name, th=_thread_id)
            print('Sending Data')
            send_time = 0
            vl.log(var='send_time', fun=_fun_name, clas=_cls_name, th=_thread_id)
            data = 'Data'
            vl.log(var='data', fun=_fun_name, clas=_cls_name, th=_thread_id)
            cca_time = chrono.read()
            vl.log(var='cca_time', fun=_fun_name, clas=_cls_name, th=_thread_id)
            cca_list.clear()
            vl.log(var='cca_list', fun=_fun_name, clas=_cls_name, th=_thread_id)


            if transmission_type == 'Unicast':
                ########### Unicast Transmission ##########################
                send_time_updated = False
                vl.log(var='send_time_updated', fun=_fun_name, clas=_cls_name, th=_thread_id)
                if ack:
                    neighbor += 1
                    vl.log(var='neighbor', fun=_fun_name, clas=_cls_name, th=_thread_id)
                if neighbor >= len(neighbor_adresses):
                    neighbor = 0
                    vl.log(var='neighbor', fun=_fun_name, clas=_cls_name, th=_thread_id)

                destination_address = neighbor_adresses[neighbor]
                vl.log(var='destination_address', fun=_fun_name, clas=_cls_name, th=_thread_id)
                safe_time = packet_gap_interval + 0.2
                vl.log(var='safe_time', fun=_fun_name, clas=_cls_name, th=_thread_id)
                channel_checked = True
                vl.log(var='channel_checked', fun=_fun_name, clas=_cls_name, th=_thread_id)
                ack = False
                vl.log(var='ack', fun=_fun_name, clas=_cls_name, th=_thread_id)
                Phase_Lock_channel_check = False
                vl.log(var='Phase_Lock_channel_check', fun=_fun_name, clas=_cls_name, th=_thread_id)
                phase_lock_transmissions = 0
                vl.log(var='phase_lock_transmissions', fun=_fun_name, clas=_cls_name, th=_thread_id)


                ############ Condition to use PLL implementation
                if destination_address in phase_lock_optimization_time and float(phase_lock_optimization_time.get(destination_address)) >= pll_activation:
                    ########### PLL optimization ##########################
                    while float(phase_lock_optimization_time.get(destination_address)) - sleep_in_pll > chrono.read():
                        lora = LoRa(power_mode=LoRa.SLEEP, region=LoRa.EU868)
                        vl.log(var='lora', fun=_fun_name, clas=_cls_name, th=_thread.get_ident())
                    while not ack and chrono.read() < max_wait_time:
                        if float(phase_lock_optimization_time.get(destination_address)) - transmission_in_pll <= chrono.read() and phase_lock_transmissions < pll_threshold:
                            ########### Transmission with PLL ##########################
                            if channel_checked:
                                phase_lock_time_saving = phase_lock_time_saving + chrono.read() - cca_time
                                vl.log(var='phase_lock_time_saving', fun=_fun_name, clas=_cls_name, th=_thread_id)
                                channel_checked = False
                                vl.log(var='channel_checked', fun=_fun_name, clas=_cls_name, th=_thread_id)
                                lora = LoRa(power_mode=LoRa.ALWAYS_ON, region=LoRa.EU868)
                                vl.log(var='lora', fun=_fun_name, clas=_cls_name, th=_thread_id)


                                if cca():
                                    ########### Channel is free and transmission with PLL starts ##########################
                                    packet1 = source_address + ' ' + ' ' + destination_address + ' ' + data + str(packet_number) + ' ' + str(send_time) + ' ' + str(chrono.read()) + ' '
                                    vl.log(var='packet1', fun=_fun_name, clas=_cls_name, th=_thread_id)
                                    padding = packet_size - len(packet1)
                                    vl.log(var='padding', fun=_fun_name, clas=_cls_name, th=_thread_id) 
                                    zero_padding = '0' * padding
                                    vl.log(var='zero_padding', fun=_fun_name, clas=_cls_name, th=_thread_id)
                                    packet = packet1 + zero_padding
                                    vl.log(var='packet', fun=_fun_name, clas=_cls_name, th=_thread_id)
                                    s.send(packet)
                                    transmissions += 1
                                    vl.log(var='transmissions', fun=_fun_name, clas=_cls_name, th=_thread_id)
                                    phase_lock_transmissions += 1
                                    vl.log(var='phase_lock_transmissions', fun=_fun_name, clas=_cls_name, th=_thread_id)
                                    print(packet1)
                                else:
                                    ########### Channel is busy ##########################
                                    phase_lock_cca_fails += 1
                                    vl.log(var='phase_lock_cca_fails', fun=_fun_name, clas=_cls_name, th=_thread_id)
                                    Phase_Lock_channel_check = True
                                    vl.log(var='Phase_Lock_channel_check', fun=_fun_name, clas=_cls_name, th=_thread_id)
                                    break
                            else:
                                packet1 = source_address + ' ' + ' ' + destination_address + ' ' + data + str(packet_number) + ' ' + str(send_time) + ' ' + str(chrono.read()) + ' '
                                vl.log(var='packet1', fun=_fun_name, clas=_cls_name, th=_thread_id)
                                padding = packet_size - len(packet1)
                                vl.log(var='padding', fun=_fun_name, clas=_cls_name, th=_thread_id)
                                zero_padding = '0' * padding
                                vl.log(var='zero_padding', fun=_fun_name, clas=_cls_name, th=_thread_id)
                                packet = packet1 + zero_padding
                                vl.log(var='packet', fun=_fun_name, clas=_cls_name, th=_thread_id)
                                s.send(packet)
                                transmissions += 1
                                vl.log(var='transmissions', fun=_fun_name, clas=_cls_name, th=_thread_id)
                                phase_lock_transmissions += 1
                                vl.log(var='phase_lock_transmissions', fun=_fun_name, clas=_cls_name, th=_thread_id)
                                print(packet1)

                        elif phase_lock_transmissions >= pll_threshold:
                            ########### If neighbour is not responding remove neighbour from PLL ##########################
                            phase_lock_optimization.pop(destination_address)
                            vl.log(var='phase_lock_optimization', fun=_fun_name, clas=_cls_name, th=_thread_id)
                            print(phase_lock_optimization)
                            phase_lock_optimization_time.pop(destination_address)
                            vl.log(var='phase_lock_optimization_time', fun=_fun_name, clas=_cls_name, th=_thread_id)
                            print(phase_lock_optimization_time)
                            break
                        else:
                            saved_transmissions += 1
                            vl.log(var='saved_transmissions', fun=_fun_name, clas=_cls_name, th=_thread_id)
                            
                        if not send_time_updated and chrono.read() > wakeup_interval - safe_time:
                            send_time_updated = True
                            vl.log(var='send_time_updated', fun=_fun_name, clas=_cls_name, th=_thread_id)
                            Full_send_time = send_time - 1
                            vl.log(var='Full_send_time', fun=_fun_name, clas=_cls_name, th=_thread_id)
                            print(Full_send_time)

                        ########### Receiving the Acknowledgement ##########################
                        time.sleep(packet_gap_interval)
                        rcv_packet1 = str(s.recv(packet_size))
                        vl.log(var='rcv_packet1', fun=_fun_name, clas=_cls_name, th=_thread_id)
                        rcv_packet1 = rcv_packet1[2:-1]
                        vl.log(var='rcv_packet1', fun=_fun_name, clas=_cls_name, th=_thread_id)
                        decode_packet = rcv_packet1.split()
                        vl.log(var='decode_packet', fun=_fun_name, clas=_cls_name, th=_thread_id)
                        if len(decode_packet) >= 5:
                            if decode_packet[3] == str(send_time) and decode_packet[1] == source_address:
                                if send_time_updated:
                                    period = int(decode_packet[4]) // Full_send_time
                                    vl.log(var='period', fun=_fun_name, clas=_cls_name, th=_thread_id)
                                    phase_lock_optimization[decode_packet[0]] = int(decode_packet[4]) - (Full_send_time + 3) * period
                                    vl.log(var='phase_lock_optimization', fun=_fun_name, clas=_cls_name, th=_thread_id)
                                else:
                                    phase_lock_optimization[decode_packet[0]] = decode_packet[4]
                                    vl.log(var='phase_lock_optimization', fun=_fun_name, clas=_cls_name, th=_thread_id)
                                    phase_lock_optimization_time[decode_packet[0]] = decode_packet[5]
                                    vl.log(var='phase_lock_optimization_time', fun=_fun_name, clas=_cls_name, th=_thread_id)
                                print(phase_lock_optimization)
                                print(phase_lock_optimization_time)
                                print('Ack received for packet {}'.format(packet_number))
                                ack_data_packets.append(rcv_packet1)
                                vl.log(var='ack_data_packets', fun=_fun_name, clas=_cls_name, th=_thread_id)
                                print(len(ack_data_packets))
                                packet_number += 1
                                vl.log(var='packet_number', fun=_fun_name, clas=_cls_name, th=_thread_id)
                                ack = True
                                vl.log(var='ack', fun=_fun_name, clas=_cls_name, th=_thread_id)
                        send_time += 1
                        vl.log(var='send_time', fun=_fun_name, clas=_cls_name, th=_thread_id)

                else:
                    ########### Transmission without PLL ##########################
                    while not ack and chrono.read() < max_wait_time:
                        ########### Transmission continue until the acknowledgement ##########################
                        packet1 = source_address + ' ' + ' ' + destination_address + ' ' + data + str(packet_number) + ' ' + str(send_time) + ' ' + str(chrono.read()) + ' '
                        vl.log(var='packet1', fun=_fun_name, clas=_cls_name, th=_thread_id)
                        padding = packet_size - len(packet1)
                        vl.log(var='padding', fun=_fun_name, clas=_cls_name, th=_thread_id)
                        zero_padding = '0' * padding
                        vl.log(var='zero_padding', fun=_fun_name, clas=_cls_name, th=_thread_id)
                        packet = packet1 + zero_padding
                        vl.log(var='packet', fun=_fun_name, clas=_cls_name, th=_thread_id)
                        s.send(packet)
                        print(packet1)
                        transmissions += 1
                        vl.log(var='transmissions', fun=_fun_name, clas=_cls_name, th=_thread_id)

                        if not send_time_updated and chrono.read() > wakeup_interval - safe_time:
                            send_time_updated = True
                            vl.log(var='send_time_updated', fun=_fun_name, clas=_cls_name, th=_thread_id)                 
                            Full_send_time = send_time - 1
                            vl.log(var='Full_send_time', fun=_fun_name, clas=_cls_name, th=_thread_id)           
                            print(Full_send_time)

                        ########### Receiving the Acknowledgement ##########################
                        time.sleep(packet_gap_interval)
                        rcv_packet1 = str(s.recv(packet_size))
                        vl.log(var='rcv_packet1', fun=_fun_name, clas=_cls_name, th=_thread_id)
                        rcv_packet1 = rcv_packet1[2:-1]
                        vl.log(var='rcv_packet1', fun=_fun_name, clas=_cls_name, th=_thread_id)
                        decode_packet = rcv_packet1.split()
                        vl.log(var='decode_packet', fun=_fun_name, clas=_cls_name, th=_thread_id)
                        print(decode_packet)
                        if len(decode_packet) >= 5:
                            print('conditions:', decode_packet[3] == str(send_time),  decode_packet[1] == source_address)
                            print(decode_packet[3], str(send_time))
                            if decode_packet[3] == str(send_time) and decode_packet[1] == source_address:
                                ########### Comment this to Disable PLL #####################
                                # if send_time_updated:
                                #     period = int(decode_packet[4]) // Full_send_time
                                #     vl.log(var='period', fun=_fun_name, clas=_cls_name, th=_thread_id)
                                #     phase_lock_optimization[decode_packet[0]] = int(decode_packet[4]) - (Full_send_time + 3) * period
                                #     vl.log(var='phase_lock_optimization', fun=_fun_name, clas=_cls_name, th=_thread_id)
                                # else:
                                #     phase_lock_optimization[decode_packet[0]] = decode_packet[4]
                                #     vl.log(var='phase_lock_optimization', fun=_fun_name, clas=_cls_name, th=_thread_id)
                                #     phase_lock_optimization_time[decode_packet[0]] = decode_packet[5]
                                #     vl.log(var='phase_lock_optimization_time', fun=_fun_name, clas=_cls_name, th=_thread_id)
                                # print(phase_lock_optimization)
                                # print(phase_lock_optimization_time)
                                print('Ack received for packet {}'.format(packet_number))

                                ack_data_packets.append(rcv_packet1)
                                vl.log(var='ack_data_packets', fun=_fun_name, clas=_cls_name, th=_thread_id)
                                print(len(ack_data_packets))
                                packet_number += 1
                                vl.log(var='packet_number', fun=_fun_name, clas=_cls_name, th=_thread_id)
                                ack = True
                                vl.log(var='ack', fun=_fun_name, clas=_cls_name, th=_thread_id)
                        send_time += 1
                        vl.log(var='send_time', fun=_fun_name, clas=_cls_name, th=_thread_id)

                if chrono.read() >= max_wait_time:
                    ########### Remove not responding neighbours ##########################
                    neighbor_adresses.remove(destination_address)
                    vl.log(var='neighbor_adresses', fun=_fun_name, clas=_cls_name, th=_thread.get_ident())
                    print(neighbor_adresses)

                if len(neighbor_adresses) == 0:
                    ########### If there are no neighbours only perform packet reception ##########################
                    only_listen = True
                    vl.log(var='only_listen', fun=_fun_name, clas=_cls_name, th=_thread.get_ident())

                if not ack and destination_address != Broadcast_address and not Phase_Lock_channel_check:
                    ########### Identify transmission failures ##########################
                    failed_attempts += 1
                    vl.log(var='failed_attempts', fun=_fun_name, clas=_cls_name, th=_thread.get_ident())              

                alive_time += chrono.read()
                vl.log(var='alive_time', fun=_fun_name, clas=_cls_name, th=_thread.get_ident())
                print('Awake_instance {}'.format(Awake_instance))
                print('Packets {}'.format(packet_number))
                print('Duty_Cycle {}'.format((alive_time / 3600) * 100))
                time_left = wakeup_interval - (chrono3.read() % wakeup_interval)
                vl.log(var='time_left', fun=_fun_name, clas=_cls_name, th=_thread.get_ident())
                chrono.stop()
                chrono.reset()
                chrono.start()
                while chrono.read() < time_left:
                    lora = LoRa(power_mode=LoRa.SLEEP, region=LoRa.EU868)
                    vl.log(var='lora', fun=_fun_name, clas=_cls_name, th=_thread.get_ident())
                    pycom.rgbled(0x7f0000)
                    pass
                lora = LoRa(power_mode=LoRa.ALWAYS_ON, region=LoRa.EU868)
                vl.log(var='lora', fun=_fun_name, clas=_cls_name, th=_thread.get_ident())
                chrono.stop()
                chrono.reset()
                print(chrono3.read())

                if chrono3.read() > wakeup_interval:
                    insatnce = chrono3.read() // wakeup_interval
                    vl.log(var='insatnce', fun=_fun_name, clas=_cls_name, th=_thread.get_ident())
                    Awake_instance += insatnce
                    vl.log(var='Awake_instance', fun=_fun_name, clas=_cls_name, th=_thread.get_ident())
                else:
                    Awake_instance += 1
                    vl.log(var='Awake_instance', fun=_fun_name, clas=_cls_name, th=_thread.get_ident())
                chrono3.stop()
                chrono3.reset()
                print(' ')

            else:
                ########### Broadcast Transmission ##########################
                print('Awake_instance {}'.format(Awake_instance))
                print('Source_address {}'.format(source_address))
                print('Packets {}'.format(packet_number))
                destination_address = Broadcast_address
                vl.log(var='destination_address', fun=_fun_name, clas=_cls_name, th=_thread_id)
                safe_time = packet_gap_interval + lora_off_time
                vl.log(var='safe_time', fun=_fun_name, clas=_cls_name, th=_thread_id)

                ########### Broadcast Transmission continue during full wake up interval ##########################
                while chrono.read() < wakeup_interval - safe_time:
                    print('chrono:', chrono.read(), wakeup_interval - safe_time)
                    data = 'Data'
                    vl.log(var='data', fun=_fun_name, clas=_cls_name, th=_thread_id)
                    packet1 = source_address + ' ' + ' ' + destination_address + ' ' + data + str(packet_number) + ' ' + str(send_time) + ' '
                    vl.log(var='packet1', fun=_fun_name, clas=_cls_name, th=_thread_id)
                    padding = packet_size - len(packet1)
                    vl.log(var='padding', fun=_fun_name, clas=_cls_name, th=_thread_id)
                    zero_padding = '0' * padding
                    vl.log(var='zero_padding', fun=_fun_name, clas=_cls_name, th=_thread_id)
                    packet = packet1 + zero_padding
                    vl.log(var='packet', fun=_fun_name, clas=_cls_name, th=_thread_id)
                    lora = LoRa(power_mode=LoRa.ALWAYS_ON, region=LoRa.EU868)
                    vl.log(var='lora', fun=_fun_name, clas=_cls_name, th=_thread_id)
                    s.send(packet)
                    print(packet1)
                    chrono2.start()
                    while chrono2.read() < packet_gap_interval:
                        lora = LoRa(power_mode=LoRa.SLEEP, region=LoRa.EU868)
                        vl.log(var='lora', fun=_fun_name, clas=_cls_name, th=_thread_id)
                    chrono2.stop()
                    chrono2.reset()
                    transmissions += 1
                    vl.log(var='transmissions', fun=_fun_name, clas=_cls_name, th=_thread_id)
                    broadcast_time_save += packet_gap_interval
                    vl.log(var='broadcast_time_save', fun=_fun_name, clas=_cls_name, th=_thread_id)
                    send_time += 1
                    vl.log(var='send_time', fun=_fun_name, clas=_cls_name, th=_thread_id)

                packet_number += 1
                vl.log(var='packet_number', fun=_fun_name, clas=_cls_name, th=_thread_id)
                alive_time += chrono.read()
                vl.log(var='alive_time', fun=_fun_name, clas=_cls_name, th=_thread_id)
                Awake_instance += 1
                vl.log(var='Awake_instance', fun=_fun_name, clas=_cls_name, th=_thread_id)
                time_left = wakeup_interval - chrono3.read()
                vl.log(var='time_left', fun=_fun_name, clas=_cls_name, th=_thread_id)
                chrono.stop()
                chrono.reset()
                chrono.start()
                while chrono.read() < time_left:
                    lora = LoRa(power_mode=LoRa.SLEEP, region=LoRa.EU868)
                    vl.log(var='lora', fun=_fun_name, clas=_cls_name, th=_thread_id)
                    pycom.rgbled(0x7f0000)
                    pass
                lora = LoRa(power_mode=LoRa.ALWAYS_ON, region=LoRa.EU868)
                vl.log(var='lora', fun=_fun_name, clas=_cls_name, th=_thread_id)
                pycom.rgbled(0x007f00)
                chrono.stop()
                chrono.reset()
                print(chrono3.read())
                chrono3.stop()
                chrono3.reset()
                print(' ')
            packet_status = False
            vl.log(var='packet_status', fun=_fun_name, clas=_cls_name, th=_thread_id)

        elif not channel_status :
            ########### Packet transmission detected and set to receive mode ##########################
            noise_found = True
            vl.log(var='noise_found', fun=_fun_name, clas=_cls_name, th=_thread_id)
            print('Receiving Data')
            time_now = chrono3.read()
            vl.log(var='time_now', fun=_fun_name, clas=_cls_name, th=_thread_id)

            ########## Fast sleep optimization ##########################
            while chrono3.read() < (packet_gap_interval * 1.1 + time_now):
                cca_list.append(str(lora.ischannel_free(-100)))
                vl.log(var='cca_list', fun=_fun_name, clas=_cls_name, th=_thread_id)
                if cca_list.count('True') <= 10 and chrono3.read() > (packet_gap_interval + time_now):
                    print(cca_list.count('True'))
                    print(chrono3.read())
                    noise_found = False
                    vl.log(var='noise_found', fun=_fun_name, clas=_cls_name, th=_thread_id)
                    print('Noise Detected')
                    noise_detected_counter += 1
                    vl.log(var='noise_detected_counter', fun=_fun_name, clas=_cls_name, th=_thread_id)
                    break
            lora = LoRa(power_mode=LoRa.ALWAYS_ON, region=LoRa.EU868)
            vl.log(var='lora', fun=_fun_name, clas=_cls_name, th=_thread_id)
            cca_list.clear()
            vl.log(var='cca_list', fun=_fun_name, clas=_cls_name, th=_thread_id)
            event = 0
            vl.log(var='event', fun=_fun_name, clas=_cls_name, th=_thread_id)
            while event != 1 and noise_found:
                event = lora.events()
                vl.log(var='event', fun=_fun_name, clas=_cls_name, th=_thread_id)
                if chrono3.read() >= fast_sleep_threshold:
                    fast_sleep_time_save += wakeup_interval - fast_sleep_threshold
                    vl.log(var='fast_sleep_time_save', fun=_fun_name, clas=_cls_name, th=_thread_id)
                    break



            ########### Packet reception ##########################
            rcv_packet = str(s.recv(packet_size))
            vl.log(var='rcv_packet', fun=_fun_name, clas=_cls_name, th=_thread_id)
            rcv_packet = rcv_packet[2:-1]
            vl.log(var='rcv_packet', fun=_fun_name, clas=_cls_name, th=_thread_id)
            decode_packet = rcv_packet.split()
            vl.log(var='decode_packet', fun=_fun_name, clas=_cls_name, th=_thread_id)
            print('decoded packet', decode_packet)
            if len(decode_packet) >= 6:
                receiving_data = decode_packet[0] + ' ' + decode_packet[2] + ' ' + decode_packet[3]
                vl.log(var='receiving_data', fun=_fun_name, clas=_cls_name, th=_thread_id)

                if decode_packet[1] == source_address:
                    ########### Unicast packet reception ##########################
                    received_full_data.append(receiving_data)
                    vl.log(var='received_full_data', fun=_fun_name, clas=_cls_name, th=_thread_id)
                    ack_packet = decode_packet[1] + ' ' + decode_packet[0] + ' Ack ' + decode_packet[3] + ' ' + decode_packet[4] + ' ' + decode_packet[5]
                    vl.log(var='ack_packet', fun=_fun_name, clas=_cls_name, th=_thread_id)
                    print('sending ack')
                    print(ack_packet)
                    s.send(ack_packet)

                elif decode_packet[1] == Broadcast_address:
                    ########### Broadcast packet reception ##########################
                    received_full_data.append(receiving_data)
                    vl.log(var='received_full_data', fun=_fun_name, clas=_cls_name, th=_thread_id)

                else:
                    print('Not For me')
            else:
                print('Unexpected Packet')
                pass

            ########### Information about received packets ##########################
            print(len(received_full_data))
            alive_time += chrono.read()
            vl.log(var='alive_time', fun=_fun_name, clas=_cls_name, th=_thread_id)
            print('Awake_instance {}'.format(Awake_instance))
            print('Source_address {}'.format(source_address))

            if len(decode_packet) >= 6:
                print('Sender_address {}'.format(decode_packet[0]))   ### source address of sender
            print('Alive_time {}'.format(alive_time))
            print('Packets {}'.format(packet_number))
            print('Duty_Cycle {}'.format((alive_time/3600)*100))

            if transmission_type == 'Unicast':
                ########### Unicast Information ##########################
                print('Packets_Received {}'.format(len(received_full_data)))
                print('failed_attempts {}'.format(failed_attempts))
                print('phase_lock_time_saving {}'.format(phase_lock_time_saving))
                print('phase_lock_cca_fails {}'.format(phase_lock_cca_fails))
                print('Optimized_Duty_Cycle_Unicast {}'.format(((alive_time - phase_lock_time_saving) / 3600) * 100))
                print('Transmissions {}'.format(transmissions + saved_transmissions))
                print('Optimized_Transmissions {}'.format(transmissions))
            else:
                ########### Broadcast Information ##########################
                print('Optimized_Duty_Cycle_broadcast {}'.format(((alive_time - broadcast_time_save) / 3600) * 100))
                print('Packets_Received {}'.format(len(received_full_data)))
                print('Transmissions {}'.format(transmissions))

            print('noise_detected_counter {}'.format(noise_detected_counter))
            print('fast_sleep_time_save {}'.format(fast_sleep_time_save))

            time_left = wakeup_interval - chrono3.read()
            vl.log(var='time_left', fun=_fun_name, clas=_cls_name, th=_thread_id)
            chrono.stop()
            chrono.reset()
            chrono.start()
            Awake_instance += 1
            vl.log(var='Awake_instance', fun=_fun_name, clas=_cls_name, th=_thread_id)
            while chrono.read() < time_left:
                pycom.rgbled(0x7f0000)
                lora = LoRa(power_mode=LoRa.SLEEP, region=LoRa.EU868)
                vl.log(var='lora', fun=_fun_name, clas=_cls_name, th=_thread_id)
                pass
            lora = LoRa(power_mode=LoRa.ALWAYS_ON, region=LoRa.EU868)
            vl.log(var='lora', fun=_fun_name, clas=_cls_name, th=_thread_id)
            pycom.rgbled(0x007f00)
            chrono.stop()
            chrono.reset()
            print(chrono3.read())
            chrono3.stop()
            chrono3.reset()
            print(' ')

        else:
            ########### No Packet to transmit so going back to sleep mode ##########################
            print('Going back to Sleep')
            print('Awake_instance {}'.format(Awake_instance))
            print('Source_address {}'.format(source_address))
            cca_list.clear()
            vl.log(var='cca_list', fun=_fun_name, clas=_cls_name, th=_thread_id)
            alive_time += chrono.read()
            vl.log(var='alive_time', fun=_fun_name, clas=_cls_name, th=_thread_id)
            print('Alive_time {}'.format(alive_time))
            print('Packets {}'.format(packet_number))
            print('Duty_Cycle {}'.format((alive_time / 3600) * 100))

            if transmission_type == 'Unicast':
                ########### Unicast Information ##########################
                print('Packets_Received {}'.format(len(received_full_data)))
                print('failed_attempts {}'.format(failed_attempts))
                print('phase_lock_time_saving {}'.format(phase_lock_time_saving))
                print('phase_lock_cca_fails {}'.format(phase_lock_cca_fails))
                print('Optimized_Duty_Cycle_Unicast {}'.format(((alive_time - phase_lock_time_saving) / 3600) * 100))
                print('Transmissions {}'.format(transmissions + saved_transmissions))
                print('Optimized_Transmissions {}'.format(transmissions))
            else:
                ########### Broadcast Information ##########################
                print('Optimized_Duty_Cycle_broadcast {}'.format(((alive_time - broadcast_time_save) / 3600) * 100))
                print('Packets_Received {}'.format(len(received_full_data)))
                print('Transmissions {}'.format(transmissions))
            print('noise_detected_counter {}'.format(noise_detected_counter))
            print('fast_sleep_time_save {}'.format(fast_sleep_time_save))
            Awake_instance += 1
            vl.log(var='Awake_instance', fun=_fun_name, clas=_cls_name, th=_thread_id)

            while chrono3.read() < wakeup_interval:
                lora = LoRa(power_mode=LoRa.SLEEP, region=LoRa.EU868)
                vl.log(var='lora', fun=_fun_name, clas=_cls_name, th=_thread_id)
                pycom.rgbled(0x7f0000)
                pass
            lora = LoRa(power_mode=LoRa.ALWAYS_ON, region=LoRa.EU868)
            vl.log(var='lora', fun=_fun_name, clas=_cls_name, th=_thread_id)
            pycom.rgbled(0x007f00)
            chrono.stop()
            chrono.reset()
            print(chrono3.read())
            chrono3.stop()
            chrono3.reset()
            print(' ')
        
        ##### for testing purposes
        if (utime.ticks_ms() - testing_start - vl.time_to_write)/1000 >= 600: # 10 minutes
            vl.save()
            print('Timer deinitiated')
            sys.exit()

    except Exception as e:
        print('Timer deinitiated')
        # write_to_log('main: {}'.format(e), str(current_time))
        print('Shutting down due to following error in main loop:')
        print(sys.print_exception(e))
        sys.exit()

