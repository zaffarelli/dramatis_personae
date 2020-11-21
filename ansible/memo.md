# Memorandum
Because I forget all of this all the time...

## System/Bash/CMD
System version (distribution)

```
cat /etc/*-release
```

Change current hostname on a *SystemD* device:
```
sudo hostnamectl set-hostname NEW_HOSTNAME
```

Disable repo:
```
yum repolist
yum --disablerepo=xxx update
```

## Postgresql
Create new postgresql user
```

```

Create new postgresql database
```

```


## Ansible specific
### Basic usage
Install module from ansible galaxy for further use:
```
ansible-galaxy collection install community.general
```
### Launch playbook
We specify the inventory **hosts** with the `i` option. The `v` option is not mandatory, it's just a verbose flag. 
It can be useful when things are going wrong.
The usage of the `i` option might be automated inside the Ansible configuration that dwells here: `/etc/ansible/ansible.cfg` 

```
ansible-playbook -v -i hosts playbook.yml
```

### others
Start service with Ansible
```

```


# LXC on raspberry PI 3B+ with centos7

## Installation
All of this come from [here](https://www.cyberciti.biz/faq/how-to-install-and-setup-lxc-linux-container-on-fedora-linux-26/)

Generic installation. Funny enough, all of this worked directly on the RPI. The fake EPEL repo might work. :-)
```
sudo dnf install lxc lxc-templates lxc-extra debootstrap libvirt perl gpg
```

Enable and check miscellaneous services.
```
sudo systemctl start libvirtd.service
sudo systemctl start lxc.service
sudo systemctl enable lxc.service
sudo systemctl status libvirtd.service
sudo systemctl status lxc.service
```

It might be angry on the last status, and would ask to modprobe config. What you in fact only have to do is exactly that:
```
modprobe config
```

## Networking
Next, let's see how we will bridge all of those containers.
```
sudo brctl show
```


It might be necessary to update the lxc.network.link by the bridge displayed with the previous command.
```
sudo vim /etc/lxc/default.conf
```

To check the range of the DHXP, please refer to:
```
sudo systemctl status libvirtd.service | grep range
```

And if everything is ok:
```
lxc-checkconfig
```

## Let's play
After that you can start using `lxc-create` commands...

Change LXC container default password:
```
chroot /opt/lxc/dp_container/rootfs passwd
```

Get the list of all available images 
```
lxc-create -t download -n NULL -- --list
```

## SSH 
### Login without password
Here are the commands to allow a@A to login without prompt has b@B.
#### Generate a key pair on A
```
a@A> ssh-keygen -t rsa
```

#### Create directory on B
```
a@A> ssh b@B mkdir -p .ssh
```

#### Append the public key from A on B
```
a@A> cat ~/.ssh/id_rsa.pub | ssh b@B 'cat >> .ssh/authorized_keys'
```

#### And ok:
```
a@A> ssh b@B
```


