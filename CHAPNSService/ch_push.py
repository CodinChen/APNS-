import time
import platform 
import codecs
import sys
import os
#发布证书
from pushjack import APNSClient
#开发证书
from pushjack import APNSSandboxClient
import json 

def push(cer,dic,isdev):
	print("cer = %s \nisdev = %s"%(cer,isdev))
	if int(isdev) == 1:
		print("开发环境")
		client = APNSSandboxClient(certificate=cer,
	                    default_error_timeout=10,
	                    default_expiration_offset=2592000,
	                    default_batch_size=100,
	                    default_retries=5)
	else:
		print("生产环境")
		client = APNSClient(certificate=cer,
	                    default_error_timeout=10,
	                    default_expiration_offset=2592000,
	                    default_batch_size=100,
	                    default_retries=5)
	

	sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
		
	res = client.send(dic['tokens'],
	                  dic['alert'],
	                  badge = dic['badge'],
	                  sound = dic['sound'],
	                  title = dic['title'],
	                  category='category',
	                  # content_available=false,
	                  mutable_content=True,
	                  # title_loc_key='t_loc_key',
	                  # title_loc_args='t_loc_args',
	                  # action_loc_key='a_loc_key',
	                  # loc_key='loc_key',
	                  extra=dic['extra']
	                  )

	print("推送结束 errors = %s"%res.errors)

def fillDictionary(str,dic):
	if "<key>" not in str:
		return
	key = str.partition('</key>')[0]
	left = str.partition('</key>')[2]

	key = key.partition('key>')[2]

	vt = left.partition('>')[0]
	left = left.partition('>')[2]
	vt = vt.partition('<')[2]

	if vt == "dict":
		value = left.partition('</dict>')[0]
		left = left.partition('</dict>')[2]
		newDic = {}
		fillDictionary(value,newDic)
		value = newDic
	elif vt == "array":
		value = left.partition('</array>')[0]
		left = left.partition('</array>')[2]
		arr = []
		for item in value.split('>'):
			if "</" in item:
				obj = item.partition('</')[0]
				arr.append(obj)
		value = arr
	else:
		value = left.partition('</%s>'%vt)[0]
		left = left.partition('</%s>'%vt)[2]

	if len(value) > 0:
		dic[key]=value
		print("key = %s \nvalue = %s"%(key,value))
	
	fillDictionary(left,dic)


if __name__ == "__main__":
	print("版本:%s"%platform.python_version())

	all_dev = sys.argv[1]
	plist = sys.argv[2]
	isdev = sys.argv[3]

	with open(plist,'r') as f:
		str = f.read()
		all = str.partition('<dict>')[2]
		dic = {}
		fillDictionary(all,dic)
		if len(dic) > 0 and (len(dic["extra"]) == 1):
			temp = dic["extra"]
			key = list(temp.keys())[0]
			value = temp[key]
			if type(value) is dict and len(value) > 0:
				value = json.dumps(value)
			dic["extra"][key] = value

		print(dic)

	
	if len(dic) > 0:
		push(all_dev,dic,isdev)	
