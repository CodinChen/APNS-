

APNS推送

python 脚本主要基于 pushjack 支持 Python3


文件目录

---------./
	ch_push.sh  推送执行脚本，里面包含一些推送证书文件路径配置
	params.plist 推送tokens和内容配置
	bin/	推送相关脚本路径
	dev/	开发环境推送证书及中间生成文件
	dis/	生产环境推送证书及中间生成文件

warnning:  
git上dev/dis 里的证书是我瞎写的文件，请自行下载导出
params.plist 中的sound 和token请根据项目情况设置，payload就随你了，开心就好

使用(以dev为例)：
1、下载aps_development.cer
2、导出cert.p12(密码设置为111111)和aps_development.cer文件一起放入./dev/文件夹下
3、./params.plist中配置目标手机apns token 及推送参数 
4、运行./ch_push.sh，默认为dev环境推送


