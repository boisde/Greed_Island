#@IgnoreInspection BashAddShebang
# CI重启STANDBY的服务们; 将目录链接指回到ACTIVE
. /root/gezbox/gezenv/bin/activate
env |grep VIRTUAL_ENV |wc -l

# 判断要重启的STANDBY
nginx_active=/root/MrWind-Configer2/nginx_conf/prod.conf
target_path_x0=prod_x0.conf
target_path_x1=prod_x1.conf

if [[ -L "${nginx_active}" && "$(readlink ${nginx_active})" = "${target_path_x0}" ]]; then
	echo "重启AG,BL,Data,Service层STANDBY: x1 group..."
    post_fix=x1
elif [[ -L "${nginx_active}"  && "$(readlink ${nginx_active})" = "${target_path_x1}" ]]; then
	echo "重启AG,BL,Data,Service层STANDBY: x0 group..."
	post_fix=x0
fi

# 重启AG,BL,Data,Service层STANDBY
# /usr/local/python27/bin/supervisorctl -s "http://localhost:9001" -u user -p 123 update
# /usr/local/python27/bin/supervisorctl -s "http://localhost:9001" -u user -p 123 restart "${post_fix}00:*"
# /usr/local/python27/bin/supervisorctl -s "http://localhost:9001" -u user -p 123 status


# 可变目录链接,这里将它指回ACTIVE
if [[ -L "${nginx_active}"  && "$(readlink ${nginx_active})" = "${target_path_x0}" ]]; then
    echo "Nginx conf linking to: [$(readlink ${nginx_active})]"
    publish_to=/root/MrWind-Dispatcher2/
elif [[ -L "${nginx_active}" && "$(readlink ${nginx_active})" = "${target_path_x1}" ]]; then
    echo "Nginx conf linking to: [$(readlink ${nginx_active})]"
    publish_to=/xvdb/MrWind-Dispatcher2/
fi
link_to_code=/root/code_dir_link
echo "Relinking [${link_to_code}] to [${publish_to}](ACTIVE)..."
cd /root
rm -rf ${link_to_code}
mkdir -p ${publish_to}
ln -s ${publish_to} code_dir_link
ls -lh