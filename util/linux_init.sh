#!/bin/bash

function selinuxDisable() {
  sed -i 's/^SELINUX\=.*$/SELINUX\=disabled/g' /etc/selinux/config
  setenforce 0
}

function snmpInit() {
# install net-snmp
yum -y install net-snmp

# snmpd.conf
cat << EOF > /etc/snmp/snmpd.conf
# COMPANY ACL
#       sec.name    source          community
com2sec local           localhost       COMPANY
com2sec cacti           14.63.196.223   COMPANY
com2sec cacti           172.27.0.122    COMPANY
com2sec icinga2         14.63.196.236   COMPANY
com2sec icinga2         172.27.0.122    COMPANY

#       sec.model                   sec.name
group   MyRWGroup       v1              local
group   MyRWGroup       v2c             local
group   MyRWGroup       usm             local
group   MyROGroup       v2c             cacti
group   MyROGroup       v2c             icinga2

#                       incl/excl       subtree mask
view all        included        .1              80

#                context sec.model sec.level match  read   write  notif
access MyROGroup ""        any       noauth    exact  all    none   none
access MyRWGroup ""        any       noauth    exact  all    all    none

syslocation Cloud Center
syscontact System Team sys@COMPANY.co.kr
EOF

# /etc/sysconfig/snmpd
sed -i 's/^OPTIONS/#\ OPTIONS/g' /etc/sysconfig/snmpd

cat << EOF >> /etc/sysconfig/snmpd
OPTIONS="-LS3d -Lf /dev/null -p /var/run/snmpd.pid"
EOF

# add systemctl
systemctl enable snmpd.service
systemctl start snmpd.service

}

function cactiInit(){
# add cacti pubkey 
cat << EOF >> /root/.ssh/authorized_keys
ssh-rsa AAAAB root@srv.localdomain
EOF

chmod 600 /root/.ssh/authorized_keys
}

function ccuInit(){
# install nrpe
yum -y install nrpe

# check_connections.sh 플러그인 설치
cd /usr/lib64/nagios/plugins/
curl -sO https://raw.githubusercontent.com/jonschipp/nagios-plugins/master/check_connections.sh
chmod 755 ./check_connections.sh

# edit nrpe.cfg
sed -i "s/^allowed_hosts\=.*$/&\,14\.63\.196\.236/g" /etc/nagios/nrpe.cfg
sed -i 's/^dont_blame_nrpe\=0/dont_blame_nrpe\=1/g' /etc/nagios/nrpe.cfg
echo "command[check_ccu]=/usr/lib64/nagios/plugins/check_connections.sh -p tcp -s established -f '( sport = :\$ARG1\$ )' -w \$ARG2\$ -c \$ARG3\$" >> /etc/nagios/nrpe.cfg

# add systemctl
systemctl enable nrpe.service
systemctl start nrpe.service
}

selinuxDisable
snmpInit
cactiInit
ccuInit

exit 0
