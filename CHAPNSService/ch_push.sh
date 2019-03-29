
#!/bin/bash

#是否开发环境
isdev=1


#获取执行脚本name
prename=${BASH_SOURCE[0]}
name=`echo $0| awk -F "/" '{ print $NF }'`
echo "执行脚本名:$name"

path=$0
path=${path%/*}

#输入
cert="${path}/dev/aps_development.cer"
p12="${path}/dev/cert.p12"

#输出
cert_pem="${path}/dev/push_cert.pem"
p12_pem="${path}/dev/push_key.pem"
all_pem="${path}/dev/all_dev.pem"

#python脚本路径
pypath="${path}/bin/ch_push.py"
#sh脚本路径
sh1="${path}/bin/ch_push_1.sh"
sh2="${path}/bin/ch_push_2.sh"

#plist路径
plist="${path}/params.plist"

if [[ $isdev -ne 1 ]]
then
	echo "=============="
	#输入
	cert="${path}/dis/aps.cer"
	p12="${path}/dis/cert.p12"

	#输出
	cert_pem="${path}/dis/push_cert.pem"
	p12_pem="${path}/dis/push_key.pem"
	all_pem="${path}/dis/all_dis.pem"
fi

#========================================================================
#========================================================================

if [ ! -f ${cert} ]
then
	echo "不存在${cert}文件,退出脚本"
	exit
fi

if [ ! -f ${p12} ]
then
	echo "不存在${p12}文件,退出脚本"
	exit
fi

#========================================================================
#========================================================================

b=0
if [ ! -f ${cert_pem} ]
then
	b=1
	echo "创建 push_cert.pem"
	openssl x509 -in ${cert} -inform der -out ${cert_pem}
fi

if [[ ! -f ${p12_pem} || $b -ne 0 ]]
then
	#需输入密码
	b=1
	echo "创建 push_key.pem"
	${sh1} "${p12}" "${p12_pem}"
fi

if [[ $b -ne 0 ]]
then
	echo "合并证书"
	cat ${cert_pem} ${p12_pem} > ${all_pem}
fi

echo "推送"
#调用python，需输入密码
${sh2} $pypath ${all_pem} ${plist} ${isdev}