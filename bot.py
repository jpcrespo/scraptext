from os import popen

def temp_gpu_rpi():
    gpu_temp = popen("vcgencmd measure_temp").readline()
    return gpu_temp.replace("\n","").replace("temp=",'gpu_temp=')

def temp_cpu_rpi():
    cpu_temp= popen("cat /sys/class/thermal/thermal_zone0/temp").readline()
    return 'cpu_temp='+str(int(cpu_temp)/1000)+'\'C'


print(temp_gpu_rpi())
print(temp_cpu_rpi())

