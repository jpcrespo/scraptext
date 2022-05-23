from os import popen

def temp_gpu_rpi():
    gpu_temp = popen("vcgencmd measure_temp").readline()
    return gpu_temp.replace("\n","")

def temp_cpu_rpi():
    cpu_temp= popen("cat /sys/class/thermal/thermal_zone0/temp").readline()
    return cpu_temp


print(temp_gpu_rpi().replace("temp=",'gpu_temp='))
print('cpu_temp='+str(int(temp_cpu_rpi())/1000)+'\'C')
