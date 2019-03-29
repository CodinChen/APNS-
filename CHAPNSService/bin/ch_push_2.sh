#!/usr/bin/expect

#可以去掉
set timeout 60
set password "123456"

#spawn在expect下执行shell脚本
#expect对通过spawn执行的shell脚本的返回进行判断，是否包含“”中的字段
#send：如果expect监测到了包含的字符串，将输入send中的内容，\n相当于回车
#interact：留在开的子进程内，可以继续输入，否则将退出子进程回到shell中（比如ssh登录到某台服务器上，只有加了interact才可以留在登录后的机器上进行操作）

spawn python3 [lindex $argv 0] [lindex $argv 1] [lindex $argv 2] [lindex $argv 3]
expect "Enter PEM pass phrase:"
send "111111\n"

interact