# -*- coding:utf-8 -*-
import xml.dom.minidom as minidom
dom = minidom.getDOMImplementation().createDocument(None,'conf',None)
root = dom.documentElement

for i in range(5):
    element = dom.createElement('plugin')
    element.appendChild(dom.createTextNode('default'))
    element.setAttribute('order', str(i))
    element.setAttribute('function', "sadasdasdasd")
    root.appendChild(element)
# 保存文件
with open('vsconfig.xml', 'w', encoding='utf-8') as f:
    dom.writexml(f, addindent='\t', newl='\n',encoding='utf-8')
