
import clr
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
clr.AddReference("System.Reflection")
from System.Reflection import Assembly

assembly = Assembly.LoadFile(R"C:\Users\Ella\Downloads\MatrixModel\DesignPatterns\DesignPatterns\bin\Debug\DesignPatterns.exe")
alltypes = assembly.GetTypes()

from collections import namedtuple
Module = namedtuple("Module",["Structors","Functionals","Interfaces","Dependencies"])

excluded = ['ToString', 'Equals', 'GetHashCode', 'GetType']
d = {}
for item in alltypes:
    if item.Namespace is None or 'Annotations' in item.Namespace or 'Program' in item.Name:
        continue
    else:
        key = item.Namespace 
        if key not in d:
            d[key] = Module([key],[],[],[])
        itemMethods = [method for method in item.GetMethods() if method.Name not in excluded]
        d[key].Structors.append(item.Name)
        d[key].Functionals.extend([n.Name for n in itemMethods])
        d[key].Interfaces.extend([(item.Name,n.Name) for n in itemMethods])
        for method in itemMethods:
            ps = [p for p in method.GetParameters()]
            param = [paraminfo.ParameterType.Name for paraminfo in ps]
            d[key].Dependencies.extend([(method.Name,par) for par in param if par and 'System' not in par])
            body = method.GetMethodBody()
            if body:
                vars= [var.LocalType.Name for var in body.LocalVariables if var.LocalType and var.LocalType.FullName and 'System' not in var.LocalType.FullName]
                d[key].Dependencies.extend([(method.Name,var)for var in vars])

Interfaces = {}
Dependencies = {}
for pattern in d:
    x = d[pattern].Structors
    if len(x) == 0:
        continue
    y = list(set(d[pattern].Functionals))
    Interfaces[pattern] = np.zeros((len(x),len(y)), dtype=np.int)
    Dependencies[pattern] = np.zeros((len(x),len(y)), dtype=np.int)
    for item,method in d[pattern].Interfaces:
        Interfaces[pattern][x.index(item),y.index(method)] = 1
    for method,item in list(set(d[pattern].Dependencies)):
        if method in y and item in x:
            Dependencies[pattern][x.index(item),y.index(method)] = 1

    fig = plt.figure(figsize = (len(x)+1,len(y)))
    fig.suptitle(pattern, fontsize=18)           
    gs = matplotlib.gridspec.GridSpec(nrows=2,ncols=1,left=0.3)

    vals = Interfaces[pattern]*-100+300

    ax1 = fig.add_subplot(gs[0])
    ax1.axis('off')
    ax1.set_title('Interfaces')
    the_table = ax1.table(cellText=Interfaces[pattern], loc='center',cellLoc='center',rowLabels=x, colLabels=y,cellColours=plt.cm.hot(vals))
    #the_table.scale(1.5, 1.5)

    vals = Dependencies[pattern]*-100+300
    ax2 = fig.add_subplot(gs[1])
    ax2.axis('off')
    ax2.set_title('Dependencies')
    the_table = ax2.table(cellText=Dependencies[pattern], loc='center',cellLoc='center',rowLabels=x, colLabels=y,cellColours=plt.cm.hot(vals))
    #the_table.scale(1.5, 1.5)
    #fig.subplots_adjust(left=0.3),colWidths=[0.15]*len(y),colWidths=[0.15]*len(y)
    plt.savefig(pattern+'.pdf')

