import os
import sys
import xml.etree.ElementTree as ET
reload(sys)
sys.setdefaultencoding('utf8')

tree = ET.parse('Inclusion-Exclusion.xml')
root = tree.getroot()

infilepath = './inclusion.txt'
exfilepath = './exclusion.txt'

ifile = open(infilepath,'a')
efile = open(exfilepath,'a')

for doc in root.findall('doc'):
    label = doc.find('label')
    label = label if(label==None) else label.text.decode('unicode-escape')

    inclusion = doc.find('inclusion')
    incl = inclusion if(inclusion==None) else inclusion.text.decode('unicode-escape')

    exclusion = doc.find('exclusion')
    excl = exclusion if(exclusion==None) else exclusion.text.decode('unicode-escape')

    if (incl!=None):
        ifile.write(label+"\n")
        ifile.write(incl+"\n")
    if (excl!=None):
        efile.write(label+"\n")
        efile.write(excl+"\n")

ifile.close()
efile.close()
