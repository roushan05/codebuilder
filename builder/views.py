# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.decorators.csrf import csrf_exempt
import json
import os
import py_compile
import logging
from . import models
logging.basicConfig(format='%(asctime)s %(message)s',filename='Events.log',level=logging.INFO)
from django.shortcuts import render
import subprocess
from subprocess import check_output
import urllib2
import requests
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()
# Create your views here.
@csrf_exempt
def home(request):
    body_data = {'foo' : "bar"}
    if request.method == "POST":
        if 'pullrequest'  not in request.body: #not a payload
            if 'path' in request.POST:
                if not (os.path.exists(request.POST['path'])):
                    return render(request, 'index.html',{'req':' ','error':'Invalid inputs.Please enter correct inputs'})
                data = models.Data()
                data.path = request.POST['path']
                data.userid = request.POST['userid']
                data.passwd = request.POST['passwd']
                data.save()
                return render(request, 'index.html')
            else:
                return render(request, 'index.html')

        else: #payload
            logging.info('Recieved a Payload')
            #body_unicode = request.body.decode('utf-8')
            body_data = json.loads(request.body)
            if body_data.has_key('pullrequest'):
                print body_data
                logging.info('Pull request payload') #send to log
                link= body_data['pullrequest']['source']['repository']['links']['html']['href']
                link = link+ '/branch/master'
                data = models.Data.objects.get(pk =1)
                os.chdir(data.path)
                subprocess.call(['git', 'fetch',link])
                logging.info('Fetched the repo')
                output = check_output(['git', 'diff', '--name-only', 'master', 'FETCH_HEAD']).split()
                subprocess.call(['git','checkout','FETCH_HEAD'])
                if compile_output(output): #no syntax errors, Merge the pr
                    try:
                        merge_link = body_data["pullrequest"]['links']["merge"]['href']
                        userid = data.userid
                        passwd = data.passwd
                        r = requests.post(merge_link, auth=('roushankr05', 'reshu5618371'))
                        if r.status_code == 200:#merged successfully
                            tagname = body_data["pullrequest"]['links']["html"]['href']
                            tagname = 'pr'+tagname[len(tagname)-1:]
                            subprocess.call(['git','tag',tagname])
                            subprocess.call(['git','push','origin',tagname])
                            logging.info('created a tag')
                        logging.info(r.status_code)
                        logging.info(r.content)
                    except Exception as e:
                        logging.info(e)
                        logging.info("failed to connect")

                else: #found syntax errors, decline the pr
                    try:
                        decline_link = body_data["pullrequest"]['links']["decline"]['href']
                        r= requests.post(decline_link, auth=(data.userid, data.passwd))
                        logging.info('Declined pull request')
                        logging.info(r.status_code)
                        logging.info(r.content)
                    except Exception as e:
                        logging.info("failed to connect")
                        logging.info(e)

            return render(request, 'index.html',{'req':body_data})
    else:
        return render(request,'index.html', {'req':"req"})

def compile_output(output):
    for i in output:
        if i[len(i)-3:]==".py":
            try:
                py_compile.compile(i,doraise=True)
            except py_compile.PyCompileError:
                logging.info("Syntax error in file")
                return False
    return True


