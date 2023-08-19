import numpy as np
import mpmath as math
import scipy.stats as stats
import csv
import psutil
import time

time1=time.time()
for proc in psutil.process_iter():
    if proc.name() == "EXCEL.EXE":
        proc.kill()

f=open("Input.txt","r")
Inputlist=(f.read())
Inputlist=Inputlist.split()
Inputlist=[float(i) for i in Inputlist]

index=[i for i in range(0,len(Inputlist)) if Inputlist[i]==-1]
Input0=[]
for j in range(0,len(index)):
    if j==0:
        dummy=Inputlist[0:index[0]]
    else:
        dummy=Inputlist[index[j-1]+1:index[j]]
    Input0.append(dummy)

def function1(scale):
    mean=scale
    cov=1
    var=(cov*mean)**2
    solx=(mean**2)/var+2
    soly=mean*(solx-1)
    return solx,soly

def function2(lifespan,maxcapa,b,decreaseCI,failurelist,yearofCI):
    a=np.mean(lifespan)/math.gamma(1+1/b)
    the_alpha,the_beta=function1(a)

    meandemand=25
    index=-1
    fail_prob=[]
    for i in np.arange(1,maxcapa-25+1+0.2,0.2):
        index=index+1
        if index==0:
            meancapa=maxcapa
        else:
            dummy=maxcapa-decreaseCI*(i-1)
            if dummy<1:
                meancapa=0
            else:
                meancapa=dummy
        stdcapa=1*meancapa
        stddemand=1*meandemand
        beta=(meancapa-meandemand)/(stdcapa**2+stddemand**2)**0.5
        fail_prob.append(stats.norm.cdf(-beta))
    the_add_year_all=[i for i in range(0,len(fail_prob)) if fail_prob[i]>failurelist]
    the_add_year=(the_add_year_all[0]+1)/5
    the_correspond_alpha=abs(-the_add_year/(abs(complex(np.log((1-failurelist))))**(1/b)))

    updated_alpha=the_alpha+yearofCI
    updated_beta=the_beta+yearofCI*the_correspond_alpha**b
    update_a=updated_beta/(updated_alpha-1)
    update_b=b
    posterior_life=stats.weibull_min.ppf(failurelist,float(update_b),loc=0,scale=float(update_a))
    y=np.arange(0,1,0.01)
    x=stats.weibull_min.ppf(y,float(update_b),loc=0,scale=float(update_a))

    return update_a,update_b,posterior_life,the_add_year,x,y


failurelist=[0.1,0.2,0.3,0.4,0.5]
for k in range(0,len(Input0)):
    Input=Input0[k]
    CSlist=Input[2::]
    final_posterior_life=[]
    finalx=[]
    for j in range(0,len(failurelist)):
        rec_life_span=[]
        temp_final_posterior_life=[]
        for i in range(0,len(CSlist)):
            if i>0:
                if CSlist[i]>CSlist[i-1]:
                    dummy=[h for h in range(0,len(CSlist[1:i-1])) if CSlist[h]==CSlist[i]]
                    if len(dummy)==0:
                        if temp_final_posterior_life[i-1]<3:
                            lifespan=[1,5]
                        else:
                            lifespan=[temp_final_posterior_life[i-1]-2,temp_final_posterior_life[i-1]+2]
                    else:
                        lifespan=rec_life_span[dummy[0]]
                else:
                    if temp_final_posterior_life[i-1]<3:
                        lifespan=[1,5]
                    else:
                        lifespan=[temp_final_posterior_life[i-1]-2,temp_final_posterior_life[i-1]+2]
            else:
                lifespan=[Input[0],Input[1]]
            rec_life_span.append(lifespan)
            maxcapa=CSlist[i]*25
            if maxcapa==25:
                maxcapa=26
            decreaseCI=25*np.mean(lifespan)**(-0.524)
            beta_s=0.05
            beta_inc=0.2
            beta_e=2.05
            index_beta=1
            prob_add_year_given_prime_weib=[]
            the_posterior_life_for_vaied_b=[]
            dummyx=[]
            for oribeta in np.arange(beta_s,beta_e+beta_inc,beta_inc):
                b=oribeta
                update_a,update_b,posterior_life,the_add_year,x,y=function2(lifespan,maxcapa,b,decreaseCI,failurelist[j],1)
                prob_add_year_given_prime_weib.append(1-abs(stats.weibull_min.cdf(the_add_year,update_b,loc=0,scale=update_a)-failurelist[j]))
                the_posterior_life_for_vaied_b.append(posterior_life)
                dummyx.append(x.tolist())
            
            updated_b_based_prob=[h/sum(prob_add_year_given_prime_weib) for h in prob_add_year_given_prime_weib]
            temp_final_posterior_life.append(sum([the_posterior_life_for_vaied_b[h]*updated_b_based_prob[h] for h in range(0,len(prob_add_year_given_prime_weib))]))
            
            if i==len(CSlist)-1 and j==len(failurelist)-1:
                tempfinalx=[]
                for h in range(0,len(dummyx)):
                    dummy=dummyx[h]
                    tempfinalx.append([dummy[g]*updated_b_based_prob[h] for g in range(0,len(dummy))])
                for h in range(0,len(tempfinalx[0])):
                    dummy=0
                    for g in range(0,len(tempfinalx)):
                        dummy=dummy+tempfinalx[g][h]
                    finalx.append(dummy)
        final_posterior_life.append(temp_final_posterior_life)

    with open('finalresult%s_1.csv'%(k+1),'w',newline='') as myfile:
        wr=csv.writer(myfile)
        for h in range(0,len(finalx)):
            wr.writerow([finalx[h],1-y[h]])

    filename='finalresult%s_2.csv'%(k+1)
    with open(filename,'w',newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        for h in final_posterior_life:
            csvwriter.writerow(h) 

print(time.time()-time1)