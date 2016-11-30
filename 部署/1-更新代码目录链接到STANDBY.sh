#!/usr/bin/env bash
# 更新代码目录软链接指向STANDBY
nginx_active=/root/MrWind-Configer/nginx_conf/prod.conf
target_path_x0=prod_x0.conf
target_path_x1=prod_x1.conf
# 可变目录链接,默认指向ACTIVE,这里会将其暂时改成指向STANDBY
link_to_code=/root/code_dir_link

if [[ -L "${nginx_active}"  && "$(readlink ${nginx_active})" = "$target_path_x0" ]]; then
    echo "Nginx conf linking to: [$(readlink ${nginx_active})]"
    publish_to=/xvdb/MrWind-Dispatcher
    echo "x0 is active, going to update x1. Publishing code to [${publish_to}]..."
elif [[ -L "${nginx_active}" && "$(readlink ${nginx_active})" = "$target_path_x1" ]]; then
    echo "Nginx conf linking to: [$(readlink ${nginx_active})]"
    publish_to=/root/MrWind-Dispatcher
    echo "x1 is active, going to update x0. Publishing code to [${publish_to}]..."
else
    # 没有任何软链接，初始化更新x0
    echo "Nginx link not found, INIT to x1..."
    # 如有,删除原有的链接
    rm -rf ${link_to_code} ${nginx_active}
    # 初始化代码目录,并创建链接
    cd /root
    publish_to=/root/MrWind-Dispatcher
    mkdir -p ${publish_to}
    ln -s ${publish_to} code_dir_link
    # 初始化nginx指向ACTIVE的链接到x1, 这样就会重启x0的代码
    cd /root/MrWind-Configer/nginx_conf
    ln -s ${target_path_x1} prod.conf
fi

# 清理STANDBY代码
rm -rf ${publish_to}/tools_lib/

# 暂时将code_dir_link指向需要更新的代码目录
echo "Temporary linking [${link_to_code}] to [${publish_to}](STANDBY)..."
rm -rf ${link_to_code}
mkdir -p ${publish_to}
cd /root/
ln -s ${publish_to} code_dir_link
ls -lh