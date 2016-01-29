#!/usr/bin/env bash
# 将6000的服务全部切换到5000上
nginx_active=/root/MrWind-Configer2/nginx_conf/prod.conf
target_path_x0=prod_x0.conf
target_path_x1=prod_x1.conf

if [[ -L "${nginx_active}"  && "$(readlink ${nginx_active})" = "$target_path_x0" ]]; then
    published=/xvdb/MrWind-Dispatcher2
    target_conf=${target_path_x1}
    echo "Switching [x1] to be [ACTIVE]. Published code in [${published}]..."
elif [[ -L "${nginx_active}" && "$(readlink ${nginx_active})" = "$target_path_x1" ]]; then
    published=/root/MrWind-Dispatcher2
    target_conf=${target_path_x0}
    echo "Switching [x0] to be [ACTIVE]. Published code in [${published}]..."
else
    echo "ERROR"
fi

# 可变目录链接,这里将它指回ACTIVE
link_to_code=/root/code_dir_link
echo "Relinking [${link_to_code}] to [${published}](ACTIVE)..."
cd /root
rm -rf ${link_to_code}
mkdir -p ${published}
ln -s ${published} code_dir_link
ls -lh

# 切换Nginx配置文件指针完成上线
echo "Relinking [${nginx_active}] to [${target_conf}]..."
cd /root/MrWind-Configer2/nginx_conf
rm -rf ${nginx_active}
ln -s ${target_conf} prod.conf
ls -lh

NP=$(cat /usr/local/nginx/logs/nginx.pid)
echo "Going to Restart -HUP Nginx[${NP}]..."
kill -HUP ${NP}