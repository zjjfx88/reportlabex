#!/bin/python
from reportlab.graphics.shapes import *
from reportlab.graphics.charts.lineplots import LinePlot
from reportlab.graphics import renderPDF
from reportlab.graphics.widgets.markers import makeMarker
from sys import argv
import string

def getLp(reportDict,init_num,height,mode):
	lp = LinePlot()
	lp.x = 100
	lp.y = height-300*(init_num+1)
	lp.height = 200
	lp.width = 400
	if mode=='used':
		lp.yValueAxis.valueMin = 0
		lp.yValueAxis.valueMax = 100
		lp.yValueAxis.valueSteps = [10,20,30,40,50,60,70,80,90,100]
	elif mode=='mem':
		lp.yValueAxis.valueMin = 0
		lp.yValueAxis.valueMax = 24000
		lp.yValueAxis.valueSteps = [2000,4000,6000,8000,10000,12000,14000,16000,18000,20000,22000,24000]
	lp.data = []
	lp.lines[0].strokeColor = colors.blue
	lst=[]
	lst_sum=[]
	xValue=[]
	infile=reportDict[0]
	with open(infile,'r') as f:
		for line in f.readlines():
			line_lst=line.split('\t')
			lst_time=float(line_lst[0])
			xValue.append(lst_time)
			lst_data=float(line_lst[1])
			lst_sum.append(lst_data)
			lst.append((lst_time,lst_data))
		lp.data.append(lst)
	avgData=round(sum(lst_sum)/len(lst_sum),2)
	lp.xValueAxis.valueMin = xValue[0]
	lp.xValueAxis.valueMax = int(xValue[-1])+1
	lp.xValueAxis.valueSteps = range(0,int(xValue[-1])+2)
	result=[]
	result.append(lp)
	result.append(avgData)
	return result

def drawReport(reportDict):
    length = len(reportDict)
    height =100 + 300*length
    drawing = Drawing(600,height)
    for init_num in range(0,length):
        data=reportDict.popitem()
	if 'gpuUsed' in data[0]:
		mode='used'
		unit='%'
	elif 'gpuMem' in data[0]:
		mode='mem'
		unit='MiB'
	else:
		mode='mode_unknown'
		unit=''
	linePlot=getLp(data,init_num,height,mode)
	print(linePlot)
        drawing.add(linePlot[0])
        drawing.add(String(220, height-300*(init_num+1)-30, data[0]+"    Avg:"+str(linePlot[1])+unit, fontSize=14, fillColor=colors.black))
        renderPDF.drawToFile(drawing, 'NvidiaInfo.pdf')

if __name__ == "__main__":
    dictreport={}
    for num in range(1,len(argv)):
        dictreport[argv[num]]=argv[num]
    print(dictreport)
    drawReport(dictreport)

