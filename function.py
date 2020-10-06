def Q_data(site_number,year1,year2):
    # input: site number
    # year1: starting year
    # year2: ending year

    # retrieve current discharge data of all stations from USGS
    import urllib
    import pandas as pd 
    import numpy as np
    import os
    import matplotlib.pyplot as plt
    #setup path
    dirname = "CFR_geomorph"
    datapath = os.getcwd()
    path = os.path.join(datapath, dirname)
    if os.path.exists(path):
        pass
    else:
        os.mkdir(path)
    filename = '/stations.csv'
    d = pd.read_csv(path+filename)

    for i in range(len(d)):
        if d['site_number'][i] == site_number:
            state_code = d['code'][i]
            historical_days = ((year2-year1)+3+(2020-year1))*365
            if len(str(site_number)) ==7:
                site_number = '0'+str(site_number)
    url='https://nwis.waterdata.usgs.gov/'+state_code+'/nwis/uv?cb_00060=on&format=rdb&site_no='+str(site_number)+'&period='+str(historical_days)
    filename = str(site_number)+'.txt'
    urllib.request.urlretrieve(url,path+filename)
    f = urllib.request.urlretrieve(url)
    df = pd.read_csv(path+filename,sep='\t',comment='#')
    for j in range(len(df.columns)):
            c = df.columns[j]
            if c[-5:] == '00060':
                index = j
    T = [_ for _ in df['datetime']]
    T = T[1:]
    Q = [_ for _ in df[df.columns[index]]]
    Q = Q[1:]
    q = []
    number = [str(_) for _ in np.arange(10)]
    for i in range(len(Q)):
        Qi=str(Q[i])
        if Qi[0] in number:
            q.append(round(float(Q[i])*0.0283168,2)) #convert cfs to m3s-1
        else:
            q.append(0)   
    Tq = pd.concat([pd.DataFrame(T),pd.DataFrame(q)],axis=1)
    Tq.columns = ['time','Q(m3s-1)']
    d_ = {}
    for j in range(len(Tq)):
        k = Tq['time'][j][0:10] 
        v = Tq['Q(m3s-1)'][j]
        d_[k] = v
    fig = plt.figure()
    ax = fig.add_subplot(111)
    Q_t =  []
    for i in np.arange(year1,year2+1,1):
        year_i = str(i)
        Y = []

        for k,v in d_.items():
            if k[0:4] == year_i:
                Y.append(v)
        Q_t.append(Y)
        ax.plot(Y,label=year_i)
        ax.set_xlim(0,365)
        ax.set_ylim(0,900)
        ax.set_xlabel('Day of year')
        ax.set_ylabel(r'Daily discharge ($m^{3} s^{-1}$)')
        ax.legend(fancybox=True,framealpha=0)
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    maxQ_ = [max(Q_t[i]) for i in range(year2-year1+1)]
    Qyear = np.arange(year1,year2+1,1)
    maxQ_.index(max(maxQ_))
    maxYear = Qyear[maxQ_.index(max(maxQ_))]
    textstr = '\n'.join(((r'$Q_{mean}:$' + str(round(sum([sum(Q_t[i]) for i in range(year2-year1+1)])/((year2-year1+1)*365),2)) + '$m^{3} s^{-1}$'),
                         (r'$Q_{peak}:$' +str(round(max(maxQ_),2))+'$m^{3} s^{-1}$'+' ('+str(maxYear)+')')))
    ax.text(0.01, 0.98, textstr, transform=ax.transAxes, fontsize=8,
        verticalalignment='top', bbox=props)
    plt.title('Data from '+str(year1)+' - '+ str(year2)+' of site number:'+str(site_number))


def plot_finer():
    import os
    import matplotlib.pyplot as plt
    #setup path
    dirname = "CFR_geomorph"
    datapath = os.getcwd()
    path = os.path.join(datapath, dirname)
    if os.path.exists(path):
        pass
    else:
        os.mkdir(path)
    filename = '/finer.csv'
    
    import pandas as pd
    d = pd.read_csv(path+filename)
    D = d['D']
    finer = d['finer']
    from matplotlib.ticker import MultipleLocator
    fig, ax = plt.subplots()
    plt.plot(D,finer, color='blue', lw=1)
    plt.xscale('log')
    plt.grid('b', which = 'minor')
    plt.grid('b', which = 'major')
    plt.ylim(0,100)
    plt.xlim(0,200)
    ax.yaxis.set_major_locator(MultipleLocator(10))
    #ax.xaxis.set_major_locator(MultipleLocator(50))
    plt.xlabel('D (mm)')
    plt.ylabel('% Finer')
    plt.show()   
    

def plot_flood_curve():
    from matplotlib.ticker import MultipleLocator
    import os
    import matplotlib.pyplot as plt
    #setup path
    dirname = "CFR_geomorph"
    datapath = os.getcwd()
    path = os.path.join(datapath, dirname)
    if os.path.exists(path):
        pass
    else:
        os.mkdir(path)
    filename = '/floodcurve.csv'

    import pandas as pd
    d = pd.read_csv(path+filename)
    ri = d['x']
    q = d['y']
    fig, ax = plt.subplots()
    #pyplot.subplot(1,1,1)
    plt.plot(ri,q, color='blue', lw=1)
    plt.xscale('log')
    plt.grid('b', which = 'minor')
    plt.grid('b', which = 'major')
    plt.ylim(0,)
    #plt.xlim(0,220)
    ax.yaxis.set_minor_locator(MultipleLocator(100))
    #ax.xaxis.set_minor_locator(MultipleLocator(10))
    plt.xlabel('RI (years)')
    plt.ylabel('Peak flow ($m^{3} s^{-1}$)')
    plt.title('Flood Frequency Curve at ClarK Fork above Missoula, MT')
    plt.show()
    
'''peak and mean discharge plot'''
#Q_data(12340500,2018,2019) #uncomment this function to run the code
'''percent finer plot'''
#plot_finer() #uncomment this function to run the code
'''flood freq curve'''
#plot_flood_curve() #uncomment this function to run the code