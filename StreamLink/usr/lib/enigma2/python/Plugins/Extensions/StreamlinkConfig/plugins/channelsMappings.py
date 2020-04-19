# -*- coding: utf-8 -*-
name2nameDict = {'telewizjawphd': 'wp'}

name2serviceDict = {'tvp1hd': '1:0:1:3ABD:514:13E:820000:0:0:0',
  }

def updateDict():
    global name2serviceDict, name2nameDict
    with open('/etc/enigma2/bouquets.tv','r') as btv:
        for bf2 in btv:
            if bf2.startswith('#SERVICE 1:7:1:0:0:0:0:0:0:0:FROM BOUQUET'):
                bf2 = bf2.split('"')[1]
                with open('/etc/enigma2/' + bf2,'r') as bf3:
                    for line in bf3:
                        if line.startswith('#SERVICE ') and '::' in line: #this excludes every url links
                            mdata = line.strip().replace('#SERVICE ','').split('::')
                            if len(mdata[1]) > 3 and not name2serviceDict.get(mdata[1], False):
                                name = mdata[1].lower().replace(' ','')
                                name = name2nameDict.get(name, name)
                                name2serviceDict[name] = mdata[0]
                                if name.endswith('hd'):
                                    name2serviceDict[name[:-2]] = mdata[0]
    name2serviceDict['updatedDict'] = True


if name2serviceDict.get('updatedDict', False) == False:
    updateDict()

if __name__ == '__main__':
    for item in name2serviceDict:
        print("Key: '{}' , Referencja: '{}'".format(item,name2serviceDict[item]))
        