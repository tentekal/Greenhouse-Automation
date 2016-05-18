import matplotlib.pyplot as plt
import matplotlib.animation as anim
from matplotlib import style
import numpy as np
style.use('fivethirtyeight')
fig = plt.figure()
def animate(i):
    xs = []
    ys = []
    zs = []
    ws = []
    sumx = 0
    sumw = 0
    sumy = 0
    sumwsquared = 0
    sumwx = 0
    sumwy = 0
    graph_data = open('alt_dhtdata.txt', 'r').read()
    lines = graph_data.split('\n')
    inc = 0
    for i in range(0, len(lines)-1):
        if len(lines[i]) > 1: #trim away empty lines
            x, y, z = lines[i].split(',')
            xs.append(x)
            ys.append(y)
            zs.append(z)
            inc+=1
            ws.append(inc)
            sumw+=float(ws[i])
            sumwsquared+=float(ws[i]**2)
            sumwx+=float(ws[i])*float(xs[i])

            sumwsquared+=float(ws[i]**2)
            sumwy+=float(ws[i])*float(ys[i])
    for j in range(0, len(xs)-1):
        sumx += float(xs[j])
        sumy += float(ys[j])
    sample = len(xs)
    a = ((sumx*sumwsquared)-(sumw*sumwx))/(sample*sumwsquared-sumw**2)
    b = ((sample*sumwx-sumw*sumx)/(sample*sumwsquared-(sumw**2)))
    c = ((sumy*sumwsquared)-(sumw*sumwy))/(sample*sumwsquared-sumw**2)
    d = ((sample*sumwy-sumw*sumy)/(sample*sumwsquared-(sumw**2)))
    linear = []
    linear2 = [] #line of best fit (ys)
    for i in range(0, len(xs)):
        temp = b*ws[i]+a #equations for ws and xs
        temp2 = c*ws[i]+d #equations for ws and ys
        linear.append(temp)
        linear2.append(temp2)
    #xs.sort()
    #ys.sort()

    #First Subplot (Temperature)
    ax1 = fig.add_subplot(2,1,1) #(size[height, 1 = largest]), size[width], position[left->right])
    ax1.clear()
    plt.xlabel("Time")
    plt.ylabel("Temperature (F)")
    ax1.plot(ws, xs, label="Temperature (F)")
    ax1.plot(ws, linear, label="Projected")#Pointless line of best fit graphed for lulz!
    legend = ax1.legend(loc='best', shadow=True)
    frame = legend.get_frame()
    frame.set_facecolor('0.90')
    for label in legend.get_texts():
        label.set_fontsize('small')

    for label in legend.get_lines():
        label.set_linewidth(1.3)
        
    #Second Sublot (Humidity)
    ax2 = fig.add_subplot(2,1,2)
    ax2.clear()
    plt.xlabel("Time")
    plt.ylabel("Humidity (%RH)")
    ax2.plot(ws, ys, label="Humidity (%RH)")
    #ax2.plot(ws, linear2, label="Projected") #Literally don't graph this junk
    legend = ax2.legend(loc='best', shadow=True)
    frame = legend.get_frame()
    frame.set_facecolor('0.90')
    # Set the fontsize
    for label in legend.get_texts():
        label.set_fontsize('small')

    for label in legend.get_lines():
        label.set_linewidth(1.3)  # the legend line width
#ani = anim.FuncAnimation(fig, animate, interval=1000)
animate(1)
plt.show()
