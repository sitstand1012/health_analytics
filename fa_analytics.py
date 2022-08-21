#coding:utf-8

from json import *
import csv
from factor_analyzer import FactorAnalyzer
#from factor_analyzer.factor_analyzer import calculate_kmo
import pandas as pd
import scipy

dir=r"C:\Users\SitSt\Downloads\archive\Key_indicator_districtwise.csv"
alldatas=[]
length=0
discardindex=[]
with open(dir) as f:
    reader = csv.reader(f)
    for i,row in enumerate(reader) :
        if i==0:
            length=len(row)
        else:
            for i in range(length):
                if row[i]=="NA":
                    discardindex.append(i)
        alldatas.append(row)

discardindex=list(set(discardindex))
discardindex.sort()
shaped_data=[]
for i in range(len(alldatas)):
    data=[]
    for j,item in enumerate(alldatas[i]):
        if j==0:
            data.append("_".join([alldatas[i][0],alldatas[i][1]]))
        elif j==1:
            pass
        elif j not in discardindex:
            data.append(item)
    shaped_data.append(data)

data_labels=shaped_data[0][1:]
shapedfilename=r"C:\Users\SitSt\Downloads\archive\Key_indicator_districtwise_shaped.csv"

with open(shapedfilename,"w",newline="") as f:
    writer=csv.writer(f)
    writer.writerows(shaped_data)

df = pd.read_csv(shapedfilename,sep=",",index_col=0)
#print(df)
dfs=df.iloc[:, :].apply(lambda x:(x-x.mean())/x.std(),axis=0)
#print(dfs)
it=0
cutprob_contribution=0.5#0.5~0.6
thr_factorweight=0.5#0.35~0.5
flag=True
print("threshold by cumlutative contribution={0}".format(cutprob_contribution))
print("threshold of factor weight={0}".format(thr_factorweight))
befcnt=len(data_labels)

print("iteration:{0} starts".format(it+1))
ei=scipy.linalg.eig(dfs.corr())[0]
ei=list(map(lambda x:float(x), ei))

allsu=sum(ei)
cum=0

for i in range(len(ei)):
    cum+=ei[i]
    if (cum/allsu)>cutprob_contribution:
        break

n_components=i+1
print("n_component={0}".format(n_components))

#kmo_val=calculate_kmo(dfs)
#print(kmo_val)

fa = FactorAnalyzer(n_factors=n_components,method="principal",rotation="geomin_obl")
fa.fit(dfs)
res = pd.DataFrame(fa.loadings_, columns=['factor{0}'.format(i+1) for i in range(n_components)])

#res["communalities"]=fa.get_communalities()
#li=fa.get_communalities().tolist()
#li.sort(reverse=True)

res.index = data_labels
for i in range(n_components):
    factor=res.loc[:,"factor{0}".format(i+1)].tolist()
    l=[]
    l2=(list(map(lambda x:pow(x,2),factor)))
    l2.sort()
    num=100*sum(l2)/len(factor)
    for j in range(len(data_labels)):
        l.append([factor[j],data_labels[j]])
        l.sort(key=lambda x:abs(x[0]),reverse=True)

for i in range(n_components):
    factor=res.loc[:,"factor{0}".format(i+1)].tolist()
    l=[]
    l2=(list(map(lambda x:pow(x,2),factor)))
    l2.sort()
    num=100*sum(l2)/len(factor)
    for j in range(len(data_labels)):
        l.append([factor[j],data_labels[j]])
    l.sort(key=lambda x:abs(x[0]),reverse=True)
    print("Print main factor(s) of factor{0}".format(i+1))
    print("contribution rate={0}".format(num))
    cnt=0
    for j in range(len(data_labels)):
        if abs(l[j][0])>=thr_factorweight:
            print(l[j])
            cnt+=1
    print("contain {0} variables".format(cnt))
    print()