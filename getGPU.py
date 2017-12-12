#!/bin/python
from datetime import datetime
from sys import argv
import os,time
now=now=datetime.now()
strfnow=now.strftime('%m%d%H%M%S')
gpuMem='gpuMem_'+strfnow
gpuUsed='gpuUsed_'+strfnow
hour=0
second=0
while True:
#	now=datetime.now()
#	strfnow=now.strftime('%d%H%M%S')
	timedata=str(hour+float('%.4f' % (float('%.4f' % second)/3600)))
	gpuInfo=os.popen('nvidia-smi | grep 250W')
	gpu_lst=gpuInfo.readlines()
	g_mem=gpu_lst[0].split()[8].split('MiB')[0]
	g_used=gpu_lst[0].split()[12].split('%')[0]
	with open(gpuMem,'a') as mem,open(gpuUsed,'a') as used:
		mem.write(timedata+"\t"+g_mem+'\n')
		used.write(timedata+"\t"+g_used+'\n')
	time.sleep(1)
	second+=1
	if second==3600:
		hour+=1
		second=0
