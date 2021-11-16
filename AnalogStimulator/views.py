from django.shortcuts import render, redirect
from django.http import HttpResponse
from matplotlib import pylab
from pylab import *
import PIL, PIL.Image
from io import *
import base64
import numpy as np
from scipy.integrate import odeint

def index(request):
    return render(request, 'index.html')

def rl(request):
    return render(request, 'rl.html')

def rc(request):
    return render(request, 'rc.html')

def buck(request):
    return render(request, 'buck.html') 

def result(request):
   

    vol = float(request.POST['voltage'])
    res = float(request.POST['Resistance'])
    ind = float(request.POST['Inductance'])

    x=np.linspace(0,25,500)
    y=np.exp(-1*res/ind*x)
    plot(x,vol*(1-y)/res)

    xlabel('Time')
    ylabel('Current')
    title('Time vs Current')
    grid(True)
    # Store image in a string buffer
    buffer = BytesIO()
    canvas = pylab.get_current_fig_manager().canvas
    canvas.draw()
    graphIMG = PIL.Image.frombytes('RGB', canvas.get_width_height(), canvas.tostring_rgb())
    graphIMG.save(buffer, "PNG")
    pylab.close()
    graphic = buffer.getvalue()
    graphic = base64.b64encode(graphic)
    buffer.close()
   
    graphic1 = vol_time1(vol, res, ind)
    return render(request, 'result.html',{'graphic': str(graphic)[2:-1], 'graphic1': str(graphic1)[2:-1]})


    #return HttpResponse (buffer.getvalue(), content_type="Image/png")


def vol_time1(vol, res, ind):
    x=np.linspace(0,25,500)
    y=np.exp(-1*res/ind*x)
    plot(x,vol*y)
    xlabel('Time')
    ylabel('Voltage')
    title('Time vs Voltage')
    grid(True)

    buffer = BytesIO()
    canvas = pylab.get_current_fig_manager().canvas
    canvas.draw()
    graphIMG = PIL.Image.frombytes('RGB', canvas.get_width_height(), canvas.tostring_rgb())
    graphIMG.save(buffer, "PNG")
    pylab.close()
    graphic1 = buffer.getvalue()
    graphic1 = base64.b64encode(graphic1)
    buffer.close()
    #print(graphic1)
    return graphic1





def resultrc(request):
       

    vol = float(request.POST['voltage'])
    res = float(request.POST['Resistance'])
    cap = float(request.POST['Capacitance'])

    x=np.linspace(0,50,500)
    y=np.exp((-1*x)/(res*cap))
    plot(x,vol*y/res)

    xlabel('Time')
    ylabel('Current')
    title('Time vs Current')
    grid(True)
    # Store image in a string buffer
    buffer = BytesIO()
    canvas = pylab.get_current_fig_manager().canvas
    canvas.draw()
    graphIMG = PIL.Image.frombytes('RGB', canvas.get_width_height(), canvas.tostring_rgb())
    graphIMG.save(buffer, "PNG")
    pylab.close()
    graphic = buffer.getvalue()
    graphic = base64.b64encode(graphic)
    buffer.close()
    
    graphic1 = vol_time2(vol, res, cap)
    return render(request, 'resultrc.html',{'graphic': str(graphic)[2:-1], 'graphic1': str(graphic1)[2:-1]})



def vol_time2(vol, res, cap):
    x=np.linspace(0,50,500)
    y=np.exp((-1*x)/(res*cap))
    plot(x,vol*(1-y))
    xlabel('Time')
    ylabel('Voltage')
    title('Time vs Voltage')
    grid(True)

    buffer = BytesIO()
    canvas = pylab.get_current_fig_manager().canvas
    canvas.draw()
    graphIMG = PIL.Image.frombytes('RGB', canvas.get_width_height(), canvas.tostring_rgb())
    graphIMG.save(buffer, "PNG")
    pylab.close()
    graphic1 = buffer.getvalue()
    graphic1 = base64.b64encode(graphic1)
    buffer.close()
    #print(graphic1)
    return graphic1

#1st approach 
# def custom_func(x_ele,Vin,L,Imax,Ton,Toff ):
#     T=Ton+Toff
#     DutyCycle= Ton/(Ton+Toff)
#     z=[]
    
#     Vout=DutyCycle*Vin
#     Imin=Imax-DutyCycle*T*((Vin-Vout)/L)
#     for x in x_ele:
#         y=x%T
        
#         if(y<Ton):
#             z.append((((Vin-Vout)/L)*y)+Imin)
#         else:
#            z.append(((-Vout/L)*y)+Imax+((Vout/L)*DutyCycle*T))
#     return z

# def resultbuck(request):
       
#     Vin = float(request.POST['voltage'])
#     # R = float(request.POST['Resistance'])
#     # C = float(request.POST['Capacitance'])
#     L = float(request.POST['Inductance'])
#     #Imin = float(request.POST['current_min'])
#     Imax = float(request.POST['current_max'])
#     Ton = float(request.POST['t_on'])
#     Toff = float(request.POST['t_off'])

    

#     x=np.linspace(0,40,5000)
#     #y=np.exp((-1*x)/(res*cap))
#     y=custom_func(x,Vin,L,Imax,Ton,Toff)
#     plot(x,y)

#     xlabel('Time')
#     ylabel('Inductor Current')
#     title('Time vs Current')
#     #ylim(Imax-20,Imax+1)
#     grid(True)
#     # Store image in a string buffer
#     buffer = BytesIO()
#     canvas = pylab.get_current_fig_manager().canvas
#     canvas.draw()
#     graphIMG = PIL.Image.frombytes('RGB', canvas.get_width_height(), canvas.tostring_rgb())
#     graphIMG.save(buffer, "PNG")
#     pylab.close()
#     graphic = buffer.getvalue()
#     graphic = base64.b64encode(graphic)
#     buffer.close()
    

#     return render(request, 'resultbuck.html',{'graphic': str(graphic)[2:-1]})

#2nd approach
# def model(volt,t,Ton,Toff,R,L,C,Vin):
#     T=Ton+Toff
#     volt1=volt[0]#Vo
#     volt2=volt[1]#dVo
#     dvolt1_dt=volt2
#     y=t%T
#     if(y<Ton):
#         dvolt2_dt=((Vin/L) - (volt1/L) - (volt2/R))/C
#         return [dvolt1_dt,dvolt2_dt]
#     else:
#         dvolt2_dt=(-(volt1/L) - (volt2/R))/C
#         return [dvolt1_dt,dvolt2_dt]

#     #return [dvolt1_dt,dvolt2_dt]


# def resultbuck(request):
       
#     Vin = float(request.POST['voltage'])
#     R = float(request.POST['Resistance'])
#     C = float(request.POST['Capacitance'])
#     L = float(request.POST['Inductance'])
#     on = float(request.POST['t_on'])
#     off = float(request.POST['t_off'])

#     L=L*.001
#     C=C*.000001
#     Ton=on*.001
#     Toff=off*.001

#     t=np.linspace(0,.01,50000)
#     volt0 = [0,0] #initial conditions
#     y=odeint(model,volt0,t,args=(Ton,Toff,R,L,C,Vin))

    
#     #y1=odeint(y[:,0],t)
#     plot(t,y[:,0])

#     xlabel('Time')
#     ylabel('Output Voltage')
#     title('Time vs Voltage')
#     grid(True)
#     # Store image in a string buffer
#     buffer = BytesIO()
#     canvas = pylab.get_current_fig_manager().canvas
#     canvas.draw()
#     graphIMG = PIL.Image.frombytes('RGB', canvas.get_width_height(), canvas.tostring_rgb())
#     graphIMG.save(buffer, "PNG")
#     pylab.close()
#     graphic = buffer.getvalue()
#     graphic = base64.b64encode(graphic)
#     buffer.close()
    

#     return render(request, 'resultbuck.html',{'graphic': str(graphic)[2:-1]})

#3rd approach
def resultbuck(request):
       
    Vin = float(request.POST['voltage'])
    R = float(request.POST['Resistance'])
    C = float(request.POST['Capacitance'])
    L = float(request.POST['Inductance'])
    on = float(request.POST['t_on'])
    off = float(request.POST['t_off'])

    L=L*.001
    C=C*.000001
    Ton=on*.001
    Toff=off*.001

    time=[0]#np.arrange(0,.01,.00001)
    Vc=[0]
    Il=[0]
    dt=.0000001
    x=np.arange(.0000001,.0300001,.0000001)
    for t in x:
        time.append(t)
        y=t%(Ton+Toff)
        if(y<=Ton):
            di=( (Vin-Vc[-1]) *dt )/L
            newI=Il[-1]+di
            Il.append(newI)
            io=Vc[-1]/R
            ic=Il[-1]-io
            dVc=(ic*dt)/C
            newV=Vc[-1]+dVc
            Vc.append(newV)
        else:
            di=((-Vc[-1])*dt)/L
            newI=Il[-1]+di
            Il.append(newI)
            io=Vc[-1]/R
            ic=Il[-1]-io
            dVc=(ic*dt)/C
            newV=Vc[-1]+dVc
            Vc.append(newV)
    
    plot(time,Vc)

    xlabel('Time')
    ylabel('Output Voltage')
    title('Time vs Voltage')
    grid(True)
    # Store image in a string buffer
    buffer = BytesIO()
    canvas = pylab.get_current_fig_manager().canvas
    canvas.draw()
    graphIMG = PIL.Image.frombytes('RGB', canvas.get_width_height(), canvas.tostring_rgb())
    graphIMG.save(buffer, "PNG")
    pylab.close()
    graphic = buffer.getvalue()
    graphic = base64.b64encode(graphic)
    buffer.close()
    

    return render(request, 'resultbuck.html',{'graphic': str(graphic)[2:-1]})