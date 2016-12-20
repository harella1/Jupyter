
# coding: utf-8

# In[3]:

import clr
clr.AddReference("System.Reflection")
from System.Reflection import Assembly


# In[4]:

assembly = Assembly.LoadFile(R"C:\Users\Ella\Downloads\MatrixModel\DesignPatterns\DesignPatterns\bin\Debug\DesignPatterns.exe")
alltypes = assembly.GetTypes()


# In[5]:

from collections import namedtuple
Module = namedtuple("Module",["Structors","Functionals", "Interfaces","Dependencies"])


# In[52]:

excluded = ['ToString', 'Equals', 'GetHashCode', 'GetType']
d = {}
for item in alltypes:
    if item.Namespace is None or 'Annotations' in item.Namespace:
        continue
    else:
        key = item.Namespace 
        if key not in d:
            d[key] = Module( [],  [], [], [])
        itemMethods = [method for method in item.GetMethods() if method.Name not in excluded]
  #      print(itemMethods)
  #      d[key].Structors.append(item.Name)
 #       d[key].Functionals.append([n.Name for n in item.GetMethods() if n.Name not in excluded])
 #       d[key].Interfaces.append([(item.Name, n.Name) for n in itemMethods])
  #      ps = [method.GetParameters() for method in itemMethods]
  #      param = [paraminfo.ParameterType.FullName for params in ps for paraminfo in params]
 #       print([(item.Name,par) for par in param if par is not None and 'System' not in par])  
  #      d[key].Dependencies.append([par for par in param if par is not None and 'System' not in par])
        body= [method.GetMethodBody() for method in itemMethods if method]
        varinmethod = [var.LocalType.Name for b in body for var in b.LocalVariables if b is not None]
        print(varinmethod)
print (len(d.keys()))
d


# In[ ]:



