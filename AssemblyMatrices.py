
import clr
import numpy as np
import matplotlib
matplotlib.use('PDF') 
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

#pp = PdfPages('matrices.pdf')

Interfaces = {}
Dependencies = {}
for pattern in d:
    x = d[pattern].Structors
    y = list(set(d[pattern].Functionals))
    Interfaces[pattern] = np.zeros((len(x),len(y)), dtype=np.int)
    Dependencies[pattern] = np.zeros((len(x),len(y)), dtype=np.int)
    for item,method in d[pattern].Interfaces:
        Interfaces[pattern][x.index(item),y.index(method)] = 1
    for method,item in list(set(d[pattern].Dependencies)):
        if method in y and item in x:
            Dependencies[pattern][x.index(item),y.index(method)] = 1

    plt.figure()
    plt.suptitle(pattern, fontsize=12)
    plt.subplot(121)
    plt.title('Interfaces')
    plt.table(cellText=Interfaces[pattern], rowLabels=x, colLabels=y, loc=(0,0), cellLoc='center')
    plt.subplot(122)
    plt.title('Dependencies')
    plt.table(cellText=Dependencies[pattern], rowLabels=x, colLabels=y,loc=(0,0), cellLoc='center')
    plt.savefig(pattern+'.pdf')

#pp.close()