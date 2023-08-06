"""

Crossed Omega, 2022-04-09

Life is pain

V1.1

"""


def graph2wav(*args, **kwargs):
    """Takes in an optional x or t array and a y array. Optional keywords: t (play time), r (sample rate), s (sound segments), l (lowest tone), h (highest tone), w (waveform), f (filter). Returns a wav array of size int(np.round_(time*samplerate)) and sample rate."""
    
    import numpy as np

    # Cleaning up the data
    y,x = argkwargcleanup(*args,**kwargs)


    # Setting up the frequency generator and arrays
    if 't' in kwargs:
        t = kwargs['t']
    else:
        t = 2

    if 'r' in kwargs:
        sr = kwargs['r']
    else:
        sr = 44100

    if 's' in kwargs:
        segs = kwargs['s']
    else:
        segs = int(100*t)

    
    # Setting up the chosen frequencies and converting XY data
    if 'l' in kwargs:
        lowT = kwargs['l']
    else:
        lowT = 130.813 # C3
    
    if 'h' in kwargs:
        highT = kwargs['h']
    else:
        highT = 2093.005 # C7
    

    # Create a frequency list for all the rows
    f_list = freqlist(y,x,lowT,highT,segs)
    
    # Synthesize all the wavs
    truepoints = int(np.round_(t*sr))
    A = np.zeros(truepoints)

    for row in f_list:
        A += synth(t,sr,segs,row,**kwargs)
        

    if 'f' in kwargs and (kwargs['f'] == 'fifth'):
        kwargs['l'],kwargs['h'] = freq2freq(lowT,7),freq2freq(highT,7)
        kwargs['f'] = ''
        Af,sf = graph2wav(*args,**kwargs)
        A += Af
        
    if 'f' in kwargs and kwargs['f'] == 'yaranaika':
        for m in [4,7,12]:
            kwargs['l'],kwargs['h'] = freq2freq(lowT,m),freq2freq(highT,m)
            kwargs['f'] = ''
            Af,sf = graph2wav(*args,**kwargs)
            A += Af

            
    A = A - A.min()
    A = A / A.max()
    
    return A,sr



def freqlist(y,x,lowT,highT,segs):

    # Libs (not owned)
    import numpy as np
    from scipy.interpolate import interp1d
    
    b = np.log(highT/lowT)
    
    if len(np.shape(x)) == 1:
        x = [x for i in range(np.shape(y)[0])]
    
    x = np.array(x)
    y = np.array(y)

    if len(np.shape(x)) == 1:
        x = [x]
    if len(np.shape(y)) == 1:
        y = [y]
    
    f_list = np.zeros((np.shape(y)[0],segs))

    for i,v in enumerate(zip(y,x)):
        yrow = v[0]
        xrow = v[1]
        
        xN = xrow - xrow.min()
        xN = xN / xN.max()

        if yrow.max() != yrow.min(): # Kind of redundant but shifts the data correction to the top of the code
            yN = yrow - yrow.min()
            yN = yN / yN.max()
        else:
            yN = yrow
        
        yM = lowT * np.exp(b * yN)

        I = interp1d(xN, yM)
        xI = np.linspace(0,1,segs)
        yI = 2 * np.pi * I(xI) # Angular to ordinal frequency
        f_list[i,:] = yI

    return f_list






def argkwargcleanup(*args,**kwargs):

    import numpy as np
    
    # Input cleanup
    class g2sError(Exception):
        pass

    # Demo
    if len(args) == 0 and len(kwargs) == 0:
        def fun(x):
            return np.maximum.reduce([-2*(x-1)**2+2,-6*(x-3)**2+6,-2*(x-5)**2+2]) #[(1-(x-1)**2)**0.5,5*(1-(x-3)**2)**0.5,(1-(x-5)**2)**0.5] # Causes imaginairy values
        y = fun(np.linspace(0,6,100))
        args = (y,)

    if not 0 < len(args) < 3:
        raise(g2sError('graph2sound takes either 1 or 2 positional arguments'))

    # Kwarg cleanup
    kwarglist = ['t','r','s','l','h','w','f']

    if len(set(kwargs).intersection(set(kwarglist))) != len(kwargs):
        raise(g2sError('Illegal keyword detected'))

    wavelist = ['sine','square','sawtooth']
    filterlist = ['','fifth','MATLAB','yaranaika']
    
    if 'w' in kwargs and kwargs['w'] not in wavelist:
        raise(g2sError('Illegal waveform detected'))

    if 'f' in kwargs and kwargs['f'] not in filterlist:
        raise(g2sError('Illegal filter detected'))
    
    
    # correctly set the args to the x and y values
    if len(args) == 1:
        y, = args
        if isinstance(y,int) or isinstance(y,float):
            raise(g2sError('You can\'t play a y singularity'))
        x = np.linspace(0,1,np.shape(y)[-1])
    if len(args) == 2:
        y,x = args
        if isinstance(y,int) or isinstance(y,float):
            raise(g2sError('You can\'t play a y singularity'))
        if isinstance(x,int) or isinstance(x,float):
            raise(g2sError('You can\'t play an x singularity'))

    # Check dimensions
    ydims = len(np.shape(y))
    xdims = len(np.shape(x))
    
    # Raggedness jesus christ this is a pain in the backend
    try:
        if len(set([len(i) for i in y])) > 1:
            raise(g2sError('The y array is ragged'))
        if len(set([len(i) for i in x])) > 1:
            raise(g2sError('The x array is ragged'))
    except Exception:
        pass
    
    if ydims > 2 or xdims > 2:
        raise(g2sError('Arrays with more than 2 dimensions are illegal'))
        
    if np.shape(x)[-1] != np.shape(y)[-1]:
        raise(g2sError('The x and y (row-wise) arrays must be of equal length'))
    
    if max(x) == min(x): # Redundant, safeguard if no time progression
        x = np.array([0,1])
        
    if max(y) == min(y): # Required: if no y progression, plays the average tone (C5)
        y = np.array([0.5]*len(x))
    
    return y,x
    


def synth(time,samplerate,segments,yI,**kwargs):

    import numpy as np
    from scipy import signal

    truepoints = int(np.round_(time*samplerate))
    pps = int(np.ceil(time * samplerate / segments)) # points per segment
    points = pps * segments
    tps = time/segments # time per segment, 6.282 (seconds)
    tpp = time/points # time per point
    

    if 'w' not in kwargs:
        kwargs['w'] = 'sine'

    filterdict = {'sine':np.sin,'square':signal.square,'sawtooth':signal.sawtooth}

    if kwargs['w'] in filterdict:
        waveform = filterdict[kwargs['w']]

    f_matlab = 0
    f_fifth = 0
    
    if 'f' in kwargs:
        if kwargs['f'] == 'MATLAB':
            f_matlab = 1
        
    phs = 0 # Fuck this parameter in particular
    A = np.zeros(points)
    
    for i in range(segments):
        A[i*pps:i*pps+pps] = (waveform(np.linspace(0,tps-tpp,pps)*yI[i] + phs))
        phs = (phs + tps*yI[i])*(1-f_matlab)

    A = A[0:truepoints]
    
    return A



def wav2sound(waveform,samplerate):
    """Takes in a waveforms and samplerate and plays back the sound it should make. Returns null."""

    import numpy as np
    
    #Backup as to not blow out your eardrums
    waveform = waveform / np.max(np.abs(waveform))

    class g2sError(Exception):
        pass
    
    try:
        import sounddevice
    except Exception:
        raise(g2sError('The sounddevice library was not found'))

    sounddevice.play(waveform, samplerate)

    return




def graph2sound(*args, **kwargs):
    """Takes in: x ot t array (optional) and a y array. Optional keywords: tone time t in s (def. 2), sample rate r in Hz (def. 44100), tone segments s (def. 100 per 1 s), lowest tone l in Hz (def. 130.8, C3), highest tone h in Hz (def. 2093, C7). Plays the sound it should make and returns null."""

    A,sr = graph2wav(*args,**kwargs)
    
    wav2sound(A,sr)
    
    return


def midi2freq(m):
    return 440*(2**((m-69)/12))

def freq2midi(f):
    import math
    return 69 + 12*math.log2(f/440)
    
def freq2freq(f,m=0):
    return midi2freq(freq2midi(f)+m)

def midi2midi(m,f=0):
    return freq2midi(midi2freq(m)+f)




if __name__ == '__main__':
    import numpy as np
    SM = [2194.2642384557125,2928.9947955360644,3287.6829951670256,3690.303226465787,4142.2213296846785,3287.6829951670256,2764.601535159018,3287.6829951670256,4388.528476911425,3690.303226465787,2928.9947955360644,2462.977224487862,2764.601535159018,2764.601535159018,2764.601535159018,2764.601535159018]
    segs = len(SM)
    t = 5
    sr = 44100
    a = synth(t,sr,segs,SM)
    wav2sound(a,sr)


    
