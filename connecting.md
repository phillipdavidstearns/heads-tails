# Connecting


This guide covers different methods for connecting to and configuring WiFi settings on the Raspberry Pi for Heads-Tails for further administration locally and remotely.


## Overview

Configuration of the WiFi settings is done using `nano` to edit the `/etc/wpa_supplicant/wpa_supplicant.conf` file. This guide assumes that the Raspberry Pi has not been preconfigured to connect to your local WiFi network.

There are two options for connecting to the Raspberry Pi 4 running Heads-Tails:

1. From the console via keyboard and mouse (easy)
1. Direct Ethernet Connection (advanced)

Once configured, connect over WiFi to manage other aspects of the Raspberry Pi:

* Check services
* Pull updates from GitHub



## Login from the Console

### Assumptions

* You are comfortable enough with the Linux command line to copy+paste or retype and run commands.
* You have obtained the appropriate credentials to login and run commands using `sudo`.

### Requirements

* A Monitor or TV that accepts HDMI input
* Micro HDMI to HDMI cable
* A USB keyboard
* Login credentials with the proper permission level to run `sudo` commands

### Getting Connected

1. Power off the Raspberry Pi
![](images/keyboard.jpg)
1. Connect the USB Keyboard to an available USB port
![](images/microHDMI.jpg)
1. Connect the Micro HDMI to HDMI cable to the left most Micro HDMI port on the Raspberry Pi 4. It should be next to the USB-C 5V power connection.
![](images/monitorHDMI.jpg)
1. Connect the HDMI end of the Micro HDMI to HDMI cable to the Monitor/TV.
1. Power on the Monitor/TV and select the appropriate HDMI input.
1. Power on the Raspberry Pi

A successful boot will display the following image on the Monitor/TV followed by the boot sequence:
![](images/raspberry-pi-boot-rainbow.png)

Not getting a boot screen? Double check your connections and equipment. It may be possible that the monitor/TV needs to support 4K. Otherwise, you may need to obtain or prepare a replacement SD card.

### Loggin In

When the boot sequence completes, you'll be prompted for the login credentials:

1. Enter the user name after the `Login:` prompt
1. Enter the password when prompted. Include spaces if necessary.

Don't have the credentials? Get in touch.

## Direct Ethernet Connection

### Assumptions

* You are using a Linux or Mac OSX host.
* You have experience using networking tools.
* You know how to download and install the appropriate required software tools on your host system.

### Requirements

* Ethernet cable
* Ethernet to USB or Thunderbolt adapter. If your host system has an ethernet port, this isn't necessary.
* the hostname of the Raspberry Pi OR `tcpdump`, a network packet capture tool
* `ssh`
* Login credentials with the proper permission level to run `sudo` commands

### Getting Connected

1. Power off the Raspberry Pi.
1. If your host system has an ethernet port, or if you already know the hostname of the Raspberry Pi, connect the ethernet cable between the host and the Raspberry Pi and skip to step 6.
1. On your host system, open a terminal and enter `ifconfig` to view the existing network interfaces.
1. Connect the ethernet adapter to your host machine and run `ifconfig`. Make note of the name of the adapter's interface e.g. `en19` or `usb1` or `eth1`.
1. Connect the ethernet cable to the host system and the Raspberry Pi
1. If you already know the hostname of the Raspberry Pi, turn on the Raspberry Pi, wait a minute for the sstem to boot, then run `ping <hostname>.local`, replacing `<hostnname>` with that of the hostname of the Raspberry Pi. If you get a successful ping, then skip to Logging In. 

```
ping -c 5 heads-tails-mulholland.local
PING heads-tails-mulholland.local (169.254.142.18): 56 data bytes
64 bytes from 169.254.142.18: icmp_seq=0 ttl=64 time=0.231 ms
64 bytes from 169.254.142.18: icmp_seq=1 ttl=64 time=0.329 ms
64 bytes from 169.254.142.18: icmp_seq=2 ttl=64 time=0.348 ms
64 bytes from 169.254.142.18: icmp_seq=3 ttl=64 time=0.278 ms
64 bytes from 169.254.142.18: icmp_seq=4 ttl=64 time=0.292 ms
--- heads-tails-mulholland.local ping statistics ---
5 packets transmitted, 5 packets received, 0.0% packet loss
round-trip min/avg/max/stddev = 0.231/0.296/0.348/0.041 ms
```

1. If you don't know the hostname, or if the ping fails, Run `sudo tcpdump -i <iface>` where `<iface>` is the name of your ethernet interface. For adapters, see previous step, for hosts with ethernet ports, it's likely that you'll use `eth0`(linux) or `en0`(Mac).
1. Turn on the Raspberry Pi and sift through the output for the IP address or the hostname of the Raspberry Pi:

```
22:17:51.710308 IP 169.254.142.18 > igmp.mcast.net: igmp v3 report, 1 group record(s)
22:17:51.965505 IP 169.254.142.18.mdns > 224.0.0.251.mdns: 0 [3q] [4n] ANY (QM)? 8.1.e.4.0.8.f.6.8.5.1.c.9.5.e.9.0.0.0.0.0.0.0.0.0.0.0.0.0.8.e.f.ip6.arpa. ANY (QM)? heads-tails-mulholland.local. ANY (QM)? 18.142.254.169.in-addr.arpa. (219)
22:17:52.011015 ARP, Request who-has 23-95-213-211-host.colocrossing.com tell 169.254.142.18, length 46
22:17:52.069567 IP6 macbook-110.local.mdns > ff02::fb.mdns: 0*- [0q] 1/0/2 (Cache flush) AAAA fe80::32:49fb:1f50:9139 (106)
22:17:52.070245 IP 169.254.142.18 > igmp.mcast.net: igmp v3 report, 1 group record(s)
22:17:52.215170 IP 169.254.142.18.mdns > 224.0.0.251.mdns: 0 [3q] [4n] ANY (QM)? 8.1.e.4.0.8.f.6.8.5.1.c.9.5.e.9.0.0.0.0.0.0.0.0.0.0.0.0.0.8.e.f.ip6.arpa. ANY (QM)? heads-tails-mulholland.local. ANY (QM)? 18.142.254.169.in-addr.arpa. (219)
22:17:52.465954 IP 169.254.142.18.mdns > 224.0.0.251.mdns: 0 [3q] [4n] ANY (QM)? 8.1.e.4.0.8.f.6.8.5.1.c.9.5.e.9.0.0.0.0.0.0.0.0.0.0.0.0.0.8.e.f.ip6.arpa. ANY (QM)? heads-tails-mulholland.local. ANY (QM)? 18.142.254.169.in-addr.arpa. (219)
22:17:52.666873 IP 169.254.142.18.mdns > 224.0.0.251.mdns: 0*- [0q] 4/0/0 (Cache flush) PTR heads-tails-mulholland.local., (Cache flush) A 169.254.142.18, (Cache flush) PTR heads-tails-mulholland.local., (Cache flush) AAAA fe80::9e59:c158:6f80:4e18 (201)
```
The example output above indicates that our Raspberry Pi is located at IP address `169.254.142.18`. Your results *will* differ.

### Loggin In

1. ssh into the Raspberry Pi by running `ssh <user>@<ip_address>`, replacing `<user>` with the Raspberry Pi username (ask the admin) and `<ip_address>` with either the hostname.local or the IP address obtained in the previous set of instructions.
1. Accept the host ssh signature by entering `yes`
1. Enter the password for the Raspberry Pi user that you obtained from the admin.

## Configuring WiFi

Edit the `wpa_supplicant.conf` file to configure the Raspberry Pi to connect to a local WiFi network.

1. run `sudo nano /etc/wpa_supplicant/wpa_supplicant.conf` to open the configuration for the wireless device in a terminal based editor.
1. Add the local network’s configuration by entering the following text to the bottom of the file. Use TAB to create indentation and use the quotes, replace the text between them.

```
network={
	ssid=“network name”
	key_mgmt=WPA-PSK
	psk=“wifi password”
	scan_ssid=1
}
```

1. Press `ctrl+x`, then `y` then `enter` to save the changes.
1. Reboot the Raspberry Pi: `sudo reboot -h now`
1. Wait for the Pi to reboot. Now log back in and enter the following command: `ip a`

You should see the `wlan0` interface is assigned an ip address, generally something like 192.168.1.123. If there’s no IP address assign to the wlan0 device, then the configuration failed. Double check the `ssid` and `password`

## Remote Management over WiFi

Once you can confirm the Raspberry Pi is connected to your local WiFi network, you can login over `ssh` from a machine connected to that same network. A caveat is that some guest networks may implement host isolation, which means that devices one the guest network will not be able to communicate with one another. This is a setting that can be changed by the admin of the WiFi network.

1. Connect to the same WiFi network as the Raspberry Pi
1. Open a terminal on your host machine.
1. Attempt to locate the RPi: `ping heads-tails-mulholland.local`
1. If you're able to get a response, then attempt to login: `ssh heads-tails@heads-tails-mulholland.local`
1. Enter the password and you should get a greeting banner and shell.

### Managing Services

The main Heads-Tails program runs as a service managed by `systemd`, located at `/lib/systemd/system/heads-tails-lite.service`. This service depends on the `pigpiod.service` also located in `/lib/systemd/system/`. By default these are enabled in order to start on boot. A third service, `wg-quick@wg0.service`, is the VPN service for remote administration.

* To check the status of the services run: `systemctl status heads-tails-lite pigpiod wg-quick@wg0`
* You should see that they are active. See below for an example of the `wg-quick@wg0` service output:

```
heads-tails@heads-tails-mulholland:~$ systemctl status wg-quick@wg0.service 
● wg-quick@wg0.service - WireGuard via wg-quick(8) for wg0
   Loaded: loaded (/lib/systemd/system/wg-quick@.service; enabled; vendor preset: enabled)
   Active: active (exited) since Fri 2020-08-21 08:03:54 EDT; 6 days ago
     Docs: man:wg-quick(8)
           man:wg(8)
           https://www.wireguard.com/
           https://www.wireguard.com/quickstart/
           https://git.zx2c4.com/WireGuard/about/src/tools/man/wg-quick.8
           https://git.zx2c4.com/WireGuard/about/src/tools/man/wg.8
  Process: 23546 ExecStart=/usr/bin/wg-quick up wg0 (code=exited, status=0/SUCCESS)
 Main PID: 23546 (code=exited, status=0/SUCCESS)
```

* If the services are either inactive, terminated, or otherwise "dead", they can be started using: `sudo systemctl start <name of the dead service>`
* Stop: `sudo systemctl stop <name of service>`
* Disable (prevent loading on boot): `sudo systemctl disable <name of service>`
* Enable (activate loading on boot): `sudo systemctl enable <name of service>`

### Updating Code

* The code base is published on [GitHub](https://github.com/phillipdavidstearns/heads-tails-lite).
* It's been cloned locally to `/home/heads-tails/heads-tails-lite`
* Change to the directory: `cd /home/heads-tails/heads-tails-lite`
* To pull in recent updates: `git pull`