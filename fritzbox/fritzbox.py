import json
from fritzconnection.lib.fritzhosts import FritzHosts
from fritzconnection.lib.fritzstatus import FritzStatus

with open('fritzbox/settings.json', 'r') as settings_file:
    settings = json.loads(settings_file.read())

fb_hosts = FritzHosts(address=settings['fritzbox_ip'], password=settings['fritzbox_pass']) # user=settings['fritzbox_user']
fb_status = FritzStatus(address=settings['fritzbox_ip'], password=settings['fritzbox_pass']) # user=settings['fritzbox_user']


def get_external_ipv4():
    external_ipv4 = fb_status.external_ip
    return external_ipv4


def get_external_ipv6():
    external_ipv6 = fb_status.external_ipv6
    return external_ipv6


def get_hosts():
    data = fb_hosts.get_hosts_info()
    hosts_all = {}
    for item in data:
        data = {
            item['name']: {
                'ip': item['ip'],
                'mac': item['mac'],
                'status': item['status']
            }
        }
        hosts_all.update(data)
    return hosts_all


def get_active_hosts():
    data = fb_hosts.get_active_hosts()
    hosts_active = {}
    for item in data:
        data = {
            item['name']: {
                'ip': item['ip'],
                'mac': item['mac'],
                'status': item['status']
            }
        }
        hosts_active.update(data)
    return hosts_active


def get_host_name_by_mac(mac_address):
    data = fb_hosts.get_host_name(mac_address)
    host_name = {'host_name': data}
    return host_name


def get_host_active_by_mac(mac_address):
    data = fb_hosts.get_host_status(mac_address)
    host_name = get_host_name_by_mac(mac_address)
    host_status = {host_name['host_name']:{"host_active": data}}
    return host_status


def get_host_info_by_mac(mac_address):
    host_info = fb_hosts.get_specific_host_entry(mac_address)
    return host_info


def get_host_info_by_ip(ip_address):
    host_info = fb_hosts.get_specific_host_entry_by_ip(ip_address)
    return host_info


def get_wol_status_by_mac(mac_address):
    host_name = get_host_name_by_mac(mac_address)
    data = fb_hosts.get_wakeonlan_status(mac_address)
    wol_status = {host_name['host_name']:{'wol_status': data}}
    return wol_status


endpoints = {
    "external_ip": "",
    "hosts_all": "",
    "hosts_active": "",
    "host_name_by_mac": {
        "error": {'error': 'no mac-address found', 'Try': '/hostname_by_mac/MAC-ADDRESS'}
    },
    "host_active_by_mac": {
        "error": {"error": "no mac-address found", "try": "/host_active_by_mac/MAC-ADDRESS"}
    },
    "host_info_by_mac": {
        "error": {'error': 'no MAC-address found', 'Try': '/host_info_by_mac/MAC-ADDRESS'}
    },
    "host_info_by_ip": {
        "error": {'error': 'no ip-address found', 'Try': '/host_info_by_ip/IP-ADDRESS'}
    },
    "wol_status_by_mac": {
        "error": {'error': 'no mac-address found', 'Try': '/wol_status_by_mac/MAC-ADDRESS'}
    }
}


def endpoint_manager(path):
    if path:
        path = path.split('/')
        if path[0] == 'external_ip':
            data = {'ipv4': get_external_ipv4(), 'ipv6': get_external_ipv6()}
            return data

        elif path[0] == 'hosts_all':
            data = get_hosts()
            return data

        elif path[0] == 'hosts_active':
            data = get_active_hosts()
            return data

        elif path[0] == 'host_name_by_mac':
            if path[1]:
                data = get_host_name_by_mac(path[1])
                return data
            else:
                data = endpoints['host_name_by_mac']['error']
                return data

        elif path[0] == 'host_active_by_mac':
            if path[1]:
                data = get_host_active_by_mac(path[1])
                return data
            else:
                data = endpoints['host_active_by_mac']['error']
                return data

        elif path[0] == 'host_info_by_mac':
            if path[1]:
                data = get_host_info_by_mac(path[1])
                return data
            else:
                data = endpoints['host_info_by_mac']['error']
                return data

        elif path[0] == 'host_info_by_ip':
            if path[1]:
                data = get_host_info_by_ip(path[1])
                return data
            else:
                data = endpoints['host_info_by_ip']['error']
                return data

        elif path[0] == 'wol_status_by_mac':
            if path[1]:
                data = get_wol_status_by_mac(path[1])
                return data
            else:
                data = endpoints['wol_status_by_mac']['error']
                return data

        else:
            endpoint_list = list(endpoints.keys())
            data = {'Error': 'endpoint not found', 'Try': endpoint_list}
            return data, 404
    else:
        endpoint_list = list(endpoints.keys())
        data = {'Error': 'endpoint not found', 'Try': endpoint_list}
        return data, 404
