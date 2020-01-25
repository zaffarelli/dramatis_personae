#!/bin/bash
echo
echo -e "\e[0;35m"
echo -e "║ ╔╦╗╔═╗                              ║"
echo -e "║  ║║╠═╝  Raspberri PI 3B+ / CentOS 7 ║"
echo -e "║ ═╩╝╩    Server Setup Script           ║"
echo -e "\e[0;m"
echo
echo -e "\e[0;35mFirewall setup...\e[0;m"
sudo firewall-cmd --permanent --add-port=80/tcp
sudo firewall-cmd --reload
echo -e "\e[0;35m...done.\e[0;m"
