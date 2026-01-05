import serial.tools.list_ports
import pynvml
import psutil
import time
import tkinter as tk
import threading

pynvml.nvmlInit()
ports = serial.tools.list_ports.comports()
mcu = serial.Serial()

portsList = []

for onePort in ports:
    portsList.append(str(onePort))
    print(str(onePort))

def update_data():
    while True:
        cpu = psutil.cpu_percent(0.3)
        #cpu = cpu * 10
        virtual_mem = psutil.virtual_memory()

        # Extract specific parameters
        total_mem = virtual_mem.total  # Total physical memory
        available_mem = virtual_mem.available  # Available physical memory
        used_mem = virtual_mem.used  # Used physical memory
        percent_mem = virtual_mem.percent  # Percentage of memory usage
        num_gpus = pynvml.nvmlDeviceGetCount()

        for gpu_id in range(num_gpus):
            # Get the GPU handle
            gpu_handle = pynvml.nvmlDeviceGetHandleByIndex(gpu_id)
            gpu_utilization = pynvml.nvmlDeviceGetUtilizationRates(gpu_handle).gpu

        print(cpu, percent_mem, gpu_utilization)
        mcu.write(f"{cpu} {percent_mem} {gpu_utilization}\n".encode('utf-8'))

def start_thread():
    # Create and start the background thread
    background_thread = threading.Thread(target=update_data)
    background_thread.start()

def closeconect():
    mcu.close()
    status_label.config(text="Serial port is not open", fg="red")

def comport():
    select = entry.get()
    print("Select Port: COM",select)
    return select

def mcustatus():
    selectedcom = comport()
    portF = "COM" + str(selectedcom)
    mcu.port = portF
    mcu.open()
    if mcu.is_open:
        print("GATE OPENED")
        status_label.config(text="Serial port is open", fg="green")
        start_thread()
    else:
        print("GATE CLOSED")
        status_label.config(text="Serial port is not open", fg="red")


window = tk.Tk()
window.title("Pc Monitoring")

entry = tk.Entry(window)
entry.pack()

status_label = tk.Label(window, text="Status: Unknown")
status_label.pack()

buttonmcu = tk.Button(window, text="Get Input", command=mcustatus)
buttonmcu.pack()
buttondisc = tk.Button(window, text="Disconnect", command=closeconect)
buttondisc.pack()

window.mainloop() 

#select = input("Select Port: COM")

#print(mcu.port)
#print(cpu)
#print(virtual_mem)
#print(available_mem)
#print(f"Utilization: {gpu_utilization}%")


#pynvml.nvmlShutdown()
    #time.sleep(0.2)
    #response = mcu.readline().decode().strip()
    #print(f"Response from mcu: {response}")


 
