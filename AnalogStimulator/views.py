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

def boost(request):
    return render(request, 'boost.html') 

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
    Vc=[5]
    Il=[0.5]
    io=[0.5]
    ic=[0.0]
    dt=.000001
    x=np.arange(.000001,.001,.000001)
    for t in x:
        time.append(t)
        y=t%(Ton+Toff)
        if(y<=Ton):
            di=( (Vin-Vc[-1]) *dt )/L
        else:
            di=((-Vc[-1])*dt)/L
            
        newI=Il[-1]+di
        Il.append(newI)
        newio=Vc[-1]/R
        io.append(newio)
        newic=Il[-1]-io[-1]
        ic.append(newic)
        dVc=(ic[-1]*dt)/C
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
    

    plot(time,Il)

    xlabel('Time')
    ylabel('Inductor Current')
    title('Time vs Current')
    grid(True)
    # Store image in a string buffer
    buffer = BytesIO()
    canvas = pylab.get_current_fig_manager().canvas
    canvas.draw()
    graphIMG = PIL.Image.frombytes('RGB', canvas.get_width_height(), canvas.tostring_rgb())
    graphIMG.save(buffer, "PNG")
    pylab.close()
    graphic1 = buffer.getvalue()
    graphic1 = base64.b64encode(graphic1)
    buffer.close()

    return render(request, 'resultbuck.html',{'graphic': str(graphic)[2:-1], 'graphic1': str(graphic1)[2:-1]})

def resultboost(request):
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
            di=( Vin *dt )/L
            newI=Il[-1]+di
            Il.append(newI)
            dVc=(-Vc[-1]*dt)/(R*C)
            newV=Vc[-1]+dVc
            Vc.append(newV)
        else:
            di=((Vin-Vc[-1])*dt)/L
            newI=Il[-1]+di
            Il.append(newI)
            dVc=((newI-(Vc[-1]/R))*dt)/C
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
    

    return render(request, 'resultboost.html',{'graphic': str(graphic)[2:-1]})