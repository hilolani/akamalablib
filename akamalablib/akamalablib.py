import numpy as np
import collections as col
import pandas as pd

def replacearray(originaltargetarray, originalsubarray, newsubarray, newsubarraydtype=np.unicode):
        import numpy as np
        newtargetarray=np.array(np.empty((len(originaltargetarray),len(newsubarray[0]))),dtype=newsubarraydtype)
        for i in range(len(originaltargetarray)):
            for j in range(len(originalsubarray)):
                if (originaltargetarray[i]==originalsubarray[j]).all():
                    newtargetarray[i]=newsubarray[j]
        return newtargetarray


def splitlist(targetlist,sublen):
    newlist=[]
    if isinstance(targetlist, list):
        newlist=np.split(np.array(targetlist), sublen)
    newlist=[newlist[i].tolist() for i in range(len(newlist))]
    return newlist            


def splitlistflex(targetlist,widthlist):
    if len(targetlist)!=sum(widthlist):
        print('The sum of widths does not mutch the length of the list.')
    else:
        sizeadjustedtmp=[]
        sizeadjusted=[0]
        j=0
        for i in widthlist:
            sizeadjustedtmp=sizeadjusted[j] + i
            sizeadjusted=np.append(sizeadjusted,sizeadjustedtmp)
            j=j+1
        sizeadjusted=np.delete(np.delete(sizeadjusted,-1),0)
        indicesingle=sizeadjusted.astype(int)
        resultarray=np.split(targetlist, indicesingle)
        result=[resultarray[i].tolist() for i in range(len(resultarray))]
        return result


def nummatrix2string(nummatrix):
    if isinstance(nummatrix[0][0],float):
        result=np.reshape(np.array([str(float(nummatrix[i][j])) for i in range(len(nummatrix)) for j in range(len(nummatrix[0]))] ).T,(len(nummatrix),len(nummatrix[0])))
    elif  isinstance(nummatrix[0][0],int):
        result=np.reshape(np.array([str(int(nummatrix[i][j])) for i in range(len(nummatrix)) for j in range(len(nummatrix[0]))] ).T,(len(nummatrix),len(nummatrix[0])))
    return result.tolist()


def strmatrix2int(strmatrix):
    result=np.reshape(np.array([int(strmatrix[i][j]) for i in range(len(strmatrix)) for j in range(len(strmatrix[0]))] ).T,(len(strmatrix),len(strmatrix[0])))
    return result.tolist()


def eyelist(i):
    return strmatrix2int((np.eye(i)).tolist())

def concat2eyelist(x,y):
    return [np.concatenate([eyelist(x)[i],eyelist(y)[j]],axis=0).tolist() for i in range(x) for j in range(y)]

def concat3eyelist(x,y,z):
    return [np.concatenate([eyelist(x)[i],eyelist(y)[j],eyelist(z)[k]],axis=0).tolist() for i in range(x) for j in range(y) for k in range(z)]

def prependlist(prelist,mainlist):
    if  len(prelist)!=len(mainlist[0]):
        print('all the input arrays must have same number of dimensions.')
    else:
        result=(np.concatenate([np.array([prelist]),np.array(mainlist)])).tolist()
        return result

def appendlist(mainlist, postlist):
    if  len(postlist)!=len(mainlist[0]):
        print('all the input arrays must have same number of dimensions.')
    else:
        result=(np.concatenate([np.array(mainlist),np.array([postlist])])).tolist()
        return result

#from https://www.mathpython.com/ja/python-list-depth/ 
def depth(k):
    if not k:
        return 0
    else:
        if isinstance(k, list):
            return 1 + max(depth(i) for i in k)
        else:
            return 0

def dividelist(list, position):
    anteriorlist=list[0:position]
    posteriorlist=list[position:]
    return [anteriorlist, posteriorlist]


def insertnestedlist(mainlist, insertedlist, position):
    if depth(mainlist)!=2:
        print("The target list for insertion should be nested.")
    elif depth(insertedlist)!=1:
        print("The list to be inserted should NOT be nested.")
    elif position>=len(mainlist):
        print("Can't insert the list:use appendlist")
    elif position<=0:
        print("Can't insert the list:use prependlist")
    else:
        divided= dividelist(mainlist,position)
        result=(np.concatenate([np.array(divided[0]),np.array([insertedlist]),np.array(divided[1])])).tolist()
        return result


def flexconcatenate(nestedlist, newpos):
    concatd=np.concatenate(nestedlist).tolist()
    divided=splitlistflex(concatd,[newpos,len(concatd)-newpos])
    return(divided)


def flatten(list,level):
    if depth(list)>level:
        tmplist=list
        for i in range(level):
            tmplist=np.concatenate(tmplist)
        return tmplist.tolist()
    else:
        print("The depth of the list is shallower than the assigned level.")


def position(list,p):
    result=[i for i, x in enumerate(list) if x == p]
    return result


def mapnumtolist(num,list):
    return [[num, x[1]] for x in enumerate(list)]


def positionindex(list):
    info=[x for x in enumerate(list)]
    tpinfo=np.transpose(info)
    uniqlist=np.unique(tpinfo[1])
    postmp=[]
    postmplist=[]
    for i in range(len(uniqlist)):
        postmp=mapnumtolist(uniqlist[i],position(tpinfo[1],uniqlist[i]))
        postmplist=(np.append(postmplist,postmp)).astype(np.int64)
    return splitlistflex(postmplist,(np.full(int(len(postmplist)/2),2,dtype=int)).tolist())   


def positionconditionned(list, filter_func):
    result=[i for i, x in enumerate(list) if filter_func(x)]
    return result


def mapthread(list1,list2,filter_func):
    result=[filter_func(x) for x in np.transpose([list1,list2]).tolist()]
    return result


def apply(list, filter_func):
    return [filter_func(x) for x in list]


def select(list, filter_func):
    return [i for i, x in enumerate(list) if filter_func(x)]


def select1(list, cond):
     return [i for i, x in enumerate(list) if eval(cond)]


def positionindexnew(list):
    ar=np.array(list)
    info=[x for x in enumerate(ar)]
    tpinfo=np.transpose(info)
    uniqlist=np.unique(tpinfo[1])
    postmplist=np.empty((2,0),dtype='str')
    for i in range(len(uniqlist)):
        postmp=np.array(mapnumtolist(uniqlist[i],position(tpinfo[1],uniqlist[i])))
        postmplist=np.insert(postmplist, postmplist.shape[1], postmp,axis=1)
    return [[x[0],x[1].astype(np.int64)] for x in np.transpose(postmplist)]


def splitdefault(list):
    posind=positionindex(list)
    sorted=[x[0] for x in posind]
    c=col.Counter(sorted)
    ckeys=c.keys()
    ckeylist=[x for x in ckeys]
    cvals=c.values()
    cvallist=[x for x in cvals]
    wolframlikesplitlist=mapthread(ckeylist,cvallist,filter_func=lambda x:([y for y in np.repeat(x[0],x[1])]))
    return  wolframlikesplitlist


def splitdefaultnew(list):
    posind=positionindexnew(list)
    sorted=[x[0] for x in posind]
    c=col.Counter(sorted)
    ckeys=c.keys()
    ckeylist=[x for x in ckeys]
    cvals=c.values()
    cvallist=[x for x in cvals]
    wolframlikesplitlist=mapthread(ckeylist,cvallist,filter_func=lambda x:([y for y in np.repeat(x[0],x[1])]))
    return  wolframlikesplitlist

def positionindexfinal(list):
    postmplist=np.array([]) 
    info=[x for x in enumerate(np.array(list))]
    tpinfo=np.transpose(info)
    uniqlist=np.unique(tpinfo[1])
    for i in range(len(uniqlist)):
        postmp=mapnumtolist(uniqlist[i],position(tpinfo[1],uniqlist[i]))
        postmplist=np.hstack((postmplist,flatten(postmp,1)))
    tmparray=np.split(postmplist, len(postmplist)/2)
    result=[[z[0],int(z[1])] for z in tmparray]
    return result

def splitdefaultfinal(list):
    posind=positionindexfinal(list)
    sorted=[x[0] for x in posind]
    c=col.Counter(sorted)
    ckeys=c.keys()
    ckeylist=[x for x in ckeys]
    cvals=c.values()
    cvallist=[x for x in cvals]
    wolframlikesplitlist=mapthread(ckeylist,cvallist,filter_func=lambda x:([y for y in np.repeat(x[0],x[1])]))
    return  wolframlikesplitlist


def bidskit_ses_prep_final(subIDlist, ordinallist=['first', 'second', 'third', 'fourth', 'fifth', 'sixth', 'seventh', 'eighth', 'ninth', 'tenth', 'eleventh', 'twelfth', 'thirteenth', 'fourteenth', 'fifteenth', 'sixteenth', 'seventeenth', 'eighteenth', 'nineteenth', 'twentieth', 'twelfth', 'thirteenth', 'fourteenth', 'fifteenth', 'sixteenth', 'seventeenth', 'eighteenth', 'nineteenth', 'twentieth']):
    lengthlist=[len(x) for x in splitdefaultfinal(subIDlist)]
    ses_series= flatten([ordinallist[0:int(x)] for x in lengthlist],1)
    return ses_series
   

def depthcomplex(k):
    #cf.https://www.mathpython.com/ja/python-list-depth/
    if not k:
        return 0
    else:
        if isinstance(k, list):
            return [1 + min(depth(i) for i in k),1 + max(depth(i) for i in k)]
        else:
            return 0

def concatflexnew(list1, list2):
    dep1=depthcomplex(list1)
    dep2=depthcomplex(list2)
    if dep1[0]==1:
        list1tmp=[list1]
    else:
        list1tmp=list1
    if dep2[0]==1:
        list2tmp=[list2]
    else:
        list2tmp=list2
    newlist=np.hstack((flatten(list1tmp,1),flatten(list2tmp,1)))
    return list(newlist)


