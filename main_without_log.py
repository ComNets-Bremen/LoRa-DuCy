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
import _thread

'''
Implemented of LoPy4/Fipy with 1.18 pycom-micropython version
'''
######### Utility Functions #######################
def get_node_id(hex=False):
    """
    Get node id, which consists of four bytes unsigned int.
    Return as hex, according to parameter.
    """
    node_id = ubinascii.hexlify(uhashlib.sha1(
        machine.unique_id()).digest()).decode("utf-8")[-8:]
    if hex:
        return node_id
    else:
        return int(node_id, 16)


######### Initialize the device #######################
lora = LoRa(mode=LoRa.LORA,power_mode=LoRa.ALWAYS_ON,region=LoRa.EU868)
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setblocking(False)
pycom.heartbeat(False)
wlan = WLAN()
wlan.deinit()
bluetooth = Bluetooth()
bluetooth.deinit()



######### Own node's information #####################
if get_node_id() == 1068904481:
    my_number=1
    source_address='Mac'+str(my_number)
    print('I am node Mac1')
elif get_node_id() == 829745241:
    my_number=2
    source_address='Mac'+str(my_number)
    print('I am node Mac2')
elif get_node_id() == 2214365277:
    my_number=3
    source_address='Mac'+str(my_number)
    print('I am node Mac3')

number_of_neighbours=2


######### Initialize the timers #######################
chrono = Timer.Chrono()
chrono1 = Timer.Chrono()
chrono2 = Timer.Chrono()
chrono3 = Timer.Chrono()

############ Configurable Parameters #################
wakeup_interval=20
fast_sleep_threshold=2.5
transmission_type='Broadcast'#Unicast or Broadcast
num_of_packets=10
pll_threshold=7
cca_duration=0.08
cca_interval=0.4
rssi_threshold=100
packet_size=255 ## bytes


############ Configuring the device ####################
packet_number=1
transmissions=0
alive_time=0
phase_lock_time_saving=0
saved_transmissions=0
failed_attempts=0
phase_lock_cca_fails=0
Awake_instance=0
broadcast_time_save=0
fast_sleep_time_save=0
Full_send_time=0
Tx_time=0
Rx_time=0
ack=False
only_listen=False
noise_detected_counter=0
ack_data_packets=[]
cca_list=[]
received_time=[]
received_full_data=[]
phase_lock_optimization={}
phase_lock_optimization_time={}
max_wait_time=1*wakeup_interval
lora_off_time=0.6
packet_gap_interval=0.5
pll_activation=2.0
sleep_in_pll=1.9
transmission_in_pll=1.8

############## Delay to avoid CCA overalap ############
number2=(wakeup_interval-2)/10
print((my_number-1)*number2)
time.sleep((my_number-1)*number2)



############## Random number generation ################
def Random():
    r = crypto.getrandbits(32)
    return ((r[0]<<24)+(r[1]<<16)+(r[2]<<8)+r[3])/4294967295.0

def RandomRange(rfrom, rto):
    return Random()*(rto-rfrom)+rfrom



############## Random packet generation ################
def packet_check(s=Awake_instance,g=packet_number,h=source_address,f=num_of_packets):
    number=int(RandomRange(1, 30))
    if packet_number<num_of_packets and 4<number<20:
        return True
    else:
        return False



############## Clear Channel Assessment ################
def cca(x=packet_gap_interval,f=lora_off_time,c=cca_list,d=chrono,l=lora,h=cca_duration,m=rssi_threshold,n=cca_interval):
    print('Checking Channel')
    chrono1.start()
    while chrono1.read()<cca_duration:
        c.append(str(lora.ischannel_free(-rssi_threshold)))
        print('RSSI during CCA {}'.format (lora.stats()[1]))
    chrono1.stop()
    chrono1.reset()
    chrono.stop()
    print('cca list', c)
    if 'False' in cca_list:
        return False
    else:
        chrono1.start()
        while chrono1.read()<cca_interval:
            l = LoRa(power_mode=LoRa.SLEEP,region=LoRa.EU868)
        l = LoRa(power_mode=LoRa.ALWAYS_ON,region=LoRa.EU868)
        chrono1.stop()
        chrono1.reset()
        chrono.start()
        chrono1.start()
        while chrono1.read()<cca_duration:
            c.append(str(lora.ischannel_free(-rssi_threshold)))
            print('RSSI during CCA {}'.format (lora.stats()[1]))
        chrono1.stop()
        chrono1.reset()
        if 'False' in cca_list:
            return False
        else:
            return True



############# Neighbor Discovery #########################
neighbour_discover=False
neighbor_adresses=[]
while not neighbour_discover:
    print('Discovering Neighbours')
    number=int(RandomRange(1, 4))
    print(number, my_number)
    if number!=my_number:
        neighbor='Mac'+str(number)
        print('Neighbor Mac{} added to the list'.format (neighbor))
        if neighbor not in neighbor_adresses:
            neighbor_adresses.append(neighbor)
            if len(neighbor_adresses)==number_of_neighbours:
                break
    time.sleep(1)
print('Neighbour Addresses:', neighbor_adresses)
Broadcast_address='All'
neighbor=0

print('Initialising Contiki MAC')
############# Contiki MAC #########################
while True:
    chrono.start()
    chrono3.start()
    channel_status=cca(chrono,cca_list)
    packet_status=packet_check(Awake_instance,packet_number)
    lora = LoRa(power_mode=LoRa.ALWAYS_ON,region=LoRa.EU868)
    while len(s.recv(packet_size))>0:
        ss=s.recv(packet_size)
        events=lora.events()

    print('Channel Status:', channel_status), 
    print('Packet Status:', packet_status)
    if channel_status and packet_status and not only_listen:
        ########### Transmit Data ##########################
        lora = LoRa(power_mode=LoRa.ALWAYS_ON,region=LoRa.EU868)
        print('Sending Data')
        send_time=0
        data = ' Data '
        cca_time=chrono.read()
        cca_list.clear()


        if transmission_type=='Unicast':
            ########### Unicast Transmission ##########################
            send_time_updated=False
            if ack:
                neighbor+=1
            if neighbor>= len(neighbor_adresses):
                neighbor=0
            destination_address=neighbor_adresses[neighbor]
            safe_time=packet_gap_interval+0.2
            channel_checked=True
            ack=False
            Phase_Lock_channel_check=False
            phase_lock_transmissions=0

            ############ Condition to use PLL implementation
            if destination_address in phase_lock_optimization_time and float(phase_lock_optimization_time.get(destination_address))>=pll_activation :
                ########### PLL optimization ##########################
                while float(phase_lock_optimization_time.get(destination_address))-sleep_in_pll > chrono.read():
                    lora = LoRa(power_mode=LoRa.SLEEP,region=LoRa.EU868)

                while not ack and chrono.read() < max_wait_time:
                    if float(phase_lock_optimization_time.get(destination_address))-transmission_in_pll <= chrono.read() and phase_lock_transmissions<pll_threshold:
                        ########### Transmission with PLL ##########################
                        if channel_checked:
                            phase_lock_time_saving=phase_lock_time_saving+chrono.read()-cca_time
                            channel_checked= False
                            lora = LoRa(power_mode=LoRa.ALWAYS_ON,region=LoRa.EU868)

                            if cca():
                                ########### Chaneel is free and transmission with PLL starts ##########################
                                packet1=source_address+' ' +' '+ destination_address+' ' + data + str(packet_number) +' '+str(send_time)+' '+str(chrono.read())+' '
                                padding=packet_size-len(packet1)
                                zero_padding='0'*padding
                                packet=packet1+zero_padding
                                s.send(packet)
                                transmissions+=1
                                phase_lock_transmissions+=1
                                print(packet1)
                            else:
                                ########### Channel is busy ##########################
                                phase_lock_cca_fails+=1
                                Phase_Lock_channel_check=True
                                break
                        else:
                            packet1=source_address+' ' +' '+ destination_address+' ' + data + str(packet_number) +' '+str(send_time)+' '+str(chrono.read())+' '
                            padding=packet_size-len(packet1)
                            zero_padding='0'*padding
                            packet=packet1+zero_padding
                            s.send(packet)
                            transmissions+=1
                            phase_lock_transmissions+=1
                            print(packet1)

                    elif phase_lock_transmissions >= pll_threshold:
                        ########### If neighbour is not responding remove neighbour from PLL ##########################
                        phase_lock_optimization.pop(destination_address)
                        print(phase_lock_optimization)
                        phase_lock_optimization_time.pop(destination_address)
                        print(phase_lock_optimization_time)
                        break
                    else:
                        saved_transmissions+=1
                    if not send_time_updated and chrono.read()> wakeup_interval-safe_time:
                        send_time_updated=True
                        Full_send_time=send_time-1
                        print(Full_send_time)

                    ########### Receiving the Acknowledgement ##########################
                    time.sleep(packet_gap_interval)
                    rcv_packet1=str(s.recv(packet_size))
                    rcv_packet1=rcv_packet1[2:-1]
                    decode_packet=rcv_packet1.split()
                    if len(decode_packet)>=5:
                        if decode_packet[3]==str(packet_number) and decode_packet[1]==source_address:
                            if send_time_updated:
                                period=int(decode_packet[4])//Full_send_time
                                phase_lock_optimization[decode_packet[0]]=int(decode_packet[4])-(Full_send_time+3)*period
                            else:
                                phase_lock_optimization[decode_packet[0]]=decode_packet[4]
                                phase_lock_optimization_time[decode_packet[0]]=decode_packet[5]
                            print(phase_lock_optimization)
                            print(phase_lock_optimization_time)
                            print('Ack received for packet {}'.format (packet_number))
                            ack_data_packets.append(rcv_packet1)
                            print(len(ack_data_packets))
                            packet_number+=1
                            ack=True
                    send_time+=1


            else:
                ########### Transmission without PLL ##########################
                while not ack and chrono.read() < max_wait_time:
                    ########### Transmission continue until the acknowledgement ##########################
                    packet1=source_address+' ' +' '+ destination_address+' ' + data + str(packet_number) +' '+str(send_time)+' '+str(chrono.read())+' '
                    padding=packet_size-len(packet1)
                    zero_padding='0'*padding
                    packet=packet1+zero_padding
                    s.send(packet)
                    print(packet1)
                    transmissions+=1

                    if not send_time_updated and chrono.read()> wakeup_interval-safe_time:
                        send_time_updated=True
                        Full_send_time=send_time-1
                        print(Full_send_time)

                    ########### Receiving the Acknowledgement ##########################
                    time.sleep(packet_gap_interval)
                    rcv_packet1=str(s.recv(packet_size))
                    rcv_packet1=rcv_packet1[2:-1]
                    decode_packet=rcv_packet1.split()
                    if len(decode_packet)>=5:
                        if decode_packet[3]==str(packet_number) and decode_packet[1]==source_address:
                            ########### Comment this to Disable PLL #####################
                            if send_time_updated:
                                period=int(decode_packet[4])//Full_send_time
                                phase_lock_optimization[decode_packet[0]]=int(decode_packet[4])-(Full_send_time+3)*period
                            else:
                                phase_lock_optimization[decode_packet[0]]=decode_packet[4]
                                phase_lock_optimization_time[decode_packet[0]]=decode_packet[5]
                            print(phase_lock_optimization)
                            print(phase_lock_optimization_time)
                            print('Ack received for packet {}'.format (packet_number))
                            ack_data_packets.append(rcv_packet1)
                            print(len(ack_data_packets))
                            packet_number+=1
                            ack=True
                    send_time+=1

            if chrono.read()>= max_wait_time:
                ########### Remove not responding neighbours ##########################
                neighbor_adresses.remove(destination_address)
                print(neighbor_adresses)

            if len(neighbor_adresses)==0:
                ########### If there are no neighbours only perform packet reception ##########################
                only_listen=True

            if not ack and destination_address !=Broadcast_address and not Phase_Lock_channel_check:
                ########### Identify transmission failures ##########################
                failed_attempts+=1


            alive_time+=chrono.read()
            print('Awake_instance {}'.format (Awake_instance))
            print('Packets {}'.format (packet_number))
            print('Duty_Cycle {}'.format ((alive_time/3600)*100))
            time_left=wakeup_interval-(chrono3.read()%wakeup_interval)
            chrono.stop()
            chrono.reset()
            chrono.start()
            while chrono.read()<time_left:
                lora = LoRa(power_mode=LoRa.SLEEP,region=LoRa.EU868)
                pycom.rgbled(0x7f0000)
                pass
            lora = LoRa(power_mode=LoRa.ALWAYS_ON,region=LoRa.EU868)
            chrono.stop()
            chrono.reset()
            print(chrono3.read())
            if chrono3.read()>wakeup_interval:
                insatnce=chrono3.read()//wakeup_interval
                Awake_instance+=insatnce
            else:
                Awake_instance+=1
            chrono3.stop()
            chrono3.reset()
            print(' ')

        else:
            ########### Broadcast Transmission ##########################
            print('Awake_instance {}'.format (Awake_instance))
            print('Source_address {}'.format (source_address))
            print('Packets {}'.format (packet_number))
            destination_address=Broadcast_address
            safe_time=packet_gap_interval+lora_off_time

            ########### Broadcast Transmission continue during full wake up interval ##########################
            while chrono.read() < wakeup_interval-safe_time:
                print('chrono:', chrono.read(), wakeup_interval-safe_time)
                data = ' Data '
                packet1=source_address+' ' +' '+ destination_address+' ' + data + str(packet_number) +' '+str(send_time)+' '
                padding=packet_size-len(packet1)
                zero_padding='0'*padding
                packet=packet1+zero_padding
                lora = LoRa(power_mode=LoRa.ALWAYS_ON,region=LoRa.EU868)
                s.send(packet)
                print(packet1)
                chrono2.start()
                while chrono2.read()<packet_gap_interval:
                    lora = LoRa(power_mode=LoRa.SLEEP,region=LoRa.EU868)
                chrono2.stop()
                chrono2.reset()
                transmissions+=1
                broadcast_time_save+=packet_gap_interval
                send_time+=1

            packet_number+=1
            alive_time+=chrono.read()
            Awake_instance+=1
            time_left= wakeup_interval-chrono3.read()
            chrono.stop()
            chrono.reset()
            chrono.start()
            while chrono.read()<time_left:
                lora = LoRa(power_mode=LoRa.SLEEP,region=LoRa.EU868)
                pycom.rgbled(0x7f0000)
                pass
            lora = LoRa(power_mode=LoRa.ALWAYS_ON,region=LoRa.EU868)
            pycom.rgbled(0x007f00)
            chrono.stop()
            chrono.reset()
            print(chrono3.read())
            chrono3.stop()
            chrono3.reset()
            print(' ')

    elif not channel_status :
        ########### Packet transmission detected and set to receive moode ##########################
        noise_found=True
        print('Receiving Data')
        time_now=chrono3.read()

        ########## Fast sleep optimization ##########################
        while chrono3.read()<(packet_gap_interval*1.1+time_now):
            cca_list.append(str(lora.ischannel_free(-100)))
            if cca_list.count('True')<=10 and chrono3.read()>(packet_gap_interval+time_now):
                print(cca_list.count('True'))
                print(chrono3.read())
                noise_found=False
                print('Noise Detected')
                noise_detected_counter+=1
                break
        lora = LoRa(power_mode=LoRa.ALWAYS_ON,region=LoRa.EU868)
        cca_list.clear()
        event=0
        while event !=1 and noise_found:
            event=lora.events()
            if chrono3.read() >= fast_sleep_threshold:
                fast_sleep_time_save+=wakeup_interval-fast_sleep_threshold
                break



        ########### Packet reception ##########################
        rcv_packet=str(s.recv(packet_size))
        rcv_packet=rcv_packet[2:-1]
        decode_packet=rcv_packet.split()
        print('decoded packet', decode_packet)
        if len(decode_packet)>=6:
            receiving_data= decode_packet[0] + ' '+decode_packet[2] +' '+decode_packet[3]

            if decode_packet[1]== source_address:
                ########### Unicast packet reception ##########################
                received_full_data.append(receiving_data)
                ack_packet= decode_packet[1] +' '+decode_packet[0]+ ' Ack ' + decode_packet[3]+' '+decode_packet[4]+' '+decode_packet[5]
                print('sending ack')
                print(ack_packet)
                s.send(ack_packet)

            elif decode_packet[1]== Broadcast_address:
                ########### Broadcast packet reception ##########################
                received_full_data.append(receiving_data)

            else:
                print('Not For me')
        else:
            print('Unexpected Packet')
            pass

        ########### Information about received packets ##########################
        print(len(received_full_data))
        alive_time+=chrono.read()
        print('Awake_instance {}'.format (Awake_instance))
        print('Source_address {}'.format (source_address))
        if len(received_full_data)>0:
            print('Sender_address {}'.format (received_full_data[-1][0]))   ### source address of sender
        print('Alive_time {}'.format (alive_time))
        print('Packets {}'.format (packet_number))
        print('Duty_Cycle {}'.format ((alive_time/3600)*100))
        if transmission_type=='Unicast':
            ########### Unicast Information ##########################
            print('Packets_Received {}'.format (len(received_full_data)))
            print('failed_attempts {}'.format (failed_attempts))
            print('phase_lock_time_saving {}'.format (phase_lock_time_saving))
            print('phase_lock_cca_fails {}'.format (phase_lock_cca_fails))
            print('Optimized_Duty_Cycle_Unicast {}'.format (((alive_time-phase_lock_time_saving)/3600)*100))
            print('Transmissions {}'.format (transmissions+saved_transmissions))
            print('Optimized_Transmissions {}'.format (transmissions))

        else:
            ########### Broadcast Information ##########################
            print('Optimized_Duty_Cycle_broadcast {}'.format (((alive_time-broadcast_time_save)/3600)*100))
            print('Packets_Received {}'.format (len(received_full_data)))
            print('Transmissions {}'.format (transmissions))

        print('noise_detected_counter {}'.format (noise_detected_counter))
        print('fast_sleep_time_save {}'.format (fast_sleep_time_save))

        time_left= wakeup_interval-chrono3.read()
        chrono.stop()
        chrono.reset()
        chrono.start()
        Awake_instance+=1
        while chrono.read()< time_left:
            pycom.rgbled(0x7f0000)
            lora = LoRa(power_mode=LoRa.SLEEP,region=LoRa.EU868)
            pass
        lora = LoRa(power_mode=LoRa.ALWAYS_ON,region=LoRa.EU868)
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
        print('Awake_instance {}'.format (Awake_instance))
        print('Source_address {}'.format (source_address))
        cca_list.clear()
        alive_time+=chrono.read()
        print('Alive_time {}'.format (alive_time))
        print('Packets {}'.format (packet_number))
        print('Duty_Cycle {}'.format ((alive_time/3600)*100))

        if transmission_type=='Unicast':
            ########### Unicast Information ##########################
            print('Packets_Received {}'.format (len(received_full_data)))
            print('failed_attempts {}'.format (failed_attempts))
            print('phase_lock_time_saving {}'.format (phase_lock_time_saving))
            print('phase_lock_cca_fails {}'.format (phase_lock_cca_fails))
            print('Optimized_Duty_Cycle_Unicast {}'.format (((alive_time-phase_lock_time_saving)/3600)*100))
            print('Transmissions {}'.format (transmissions+saved_transmissions))
            print('Optimized_Transmissions {}'.format (transmissions))

        else:
            ########### Broadcast Information ##########################
            print('Optimized_Duty_Cycle_broadcast {}'.format (((alive_time-broadcast_time_save)/3600)*100))
            print('Packets_Received {}'.format (len(received_full_data)))
            print('Transmissions {}'.format (transmissions))
        print('noise_detected_counter {}'.format (noise_detected_counter))
        print('fast_sleep_time_save {}'.format (fast_sleep_time_save))
        Awake_instance+=1
        while chrono3.read()< wakeup_interval:
            lora = LoRa(power_mode=LoRa.SLEEP,region=LoRa.EU868)
            pycom.rgbled(0x7f0000)
            pass
        lora = LoRa(power_mode=LoRa.ALWAYS_ON,region=LoRa.EU868)
        pycom.rgbled(0x007f00)
        chrono.stop()
        chrono.reset()
        print(chrono3.read())
        chrono3.stop()
        chrono3.reset()
        print(' ')
