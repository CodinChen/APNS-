#!/usr/bin/expect

set timeout 20

set password "123456"

spawn openssl pkcs12 -in [lindex $argv 0] -out [lindex $argv 1] -nodes

expect "Enter Import Password:"
send "111111\n"

interact