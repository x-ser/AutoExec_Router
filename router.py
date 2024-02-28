from configparser import ConfigParser
import netmiko
import json, sys, subprocess

config = ConfigParser()

if sys.version[0] == "2":
    exit("\n    Script is not supported for python 2.x\n")

def debug(text, mode):
    if mode == 'alert':
        print('\033[1;33;40m [ALERT] \033[1;37;40m'+text)
        # print('\033[1;37;40m')
    elif mode == 'message':
        print('\033[1;34;40m [MESSAGE] \033[1;37;40m'+text)
    elif mode == 'suscess':
        print('\033[1;32;40m [SUSCESS] \033[1;37;40m'+text)
        # print('\033[1;37;40m')
    elif mode == 'error':
        print('\033[1;31m [ERROR] \033[1;37;40m'+text)
        # print('\033[1;37;40m')

def create_json():
    config.read('config.ini')
    sections = [key for key in config.sections()]
    list_host = []
    for section in sections:
        item = config.items(section)
        jsondata = dict(item)
        data = [section,json.dumps(jsondata)]
        list_host.append(data)
        config.remove_section(section)
    return list_host

def excute_command(host,ssh_Host):
    config.read('command.ini')
    # result = ssh_Host.send_command(command)
    sections = [i for i in config['COMMAND']]
    # debug()
    for section in sections: 
        command = config['COMMAND'][section]
        result = ssh_Host.send_command(command)
        # result = 'xxxxxx'
        debug(f'Commad: {command} Send to [\033[1;35;40m{host}\033[1;37;40m]', 'alert')
        debug(f'{result}', 'message')

def check_host(host):
    try:
        result = subprocess.run(['ping', host], capture_output=True, text=True)
        # print(result)
        if result.returncode == 0:
            debug(f'Host is \033[32mAlive\033[1;37;40m (\033[1;35;40m{host}\033[1;37;40m)', 'alert')
            return True
        else:
            debug(f'Host is \33[91mDown\033[1;37;40m (\033[1;35;40m{host}\033[1;37;40m)', 'alert')
            return False
    except:
        return False
    
def connect_Host(hosts):
    for host,data in hosts:
        address = json.loads(data)['host']
        if check_host(address):
            try: 
                debug(f'Conecting to \033[1;35;40m{address}\033[1;37;40m', 'alert')
                ssh_Host = netmiko.ConnectHandler(**json.loads(data))
                ssh_Host.enable()
                debug(f'Conect to \033[1;35;40m{host}\033[1;37;40m', 'suscess')
                excute_command(host, ssh_Host)
            except netmiko.exceptions.NetmikoTimeoutException:
                debug(f"Can't Connect to \033[1;36;40m{host}\033[1;37;40m, Please Check \033[1;36;40mConfig.ini\033[1;37;40m", 'error')

def main():
    hosts = create_json()
    # print(hosts)
    connect_Host(hosts)

def banner():
    RED = "\33[91m"
    BLUE = "\33[94m"
    GREEN = "\033[32m"
    YELLOW = "\033[93m"
    PURPLE = '\033[0;35m' 
    CYAN = "\033[36m"
    END = "\033[0m"

    fonts = f'''
    {CYAN}
        
    ██████╗  ██████╗ ██╗   ██╗████████╗███████╗██████╗ 
    ██╔══██╗██╔═══██╗██║   ██║╚══██╔══╝██╔════╝██╔══██╗
    ██████╔╝██║   ██║██║   ██║   ██║   █████╗  ██████╔╝
    ██╔══██╗██║   ██║██║   ██║   ██║   ██╔══╝  ██╔══██╗
    ██║  ██║╚██████╔╝╚██████╔╝   ██║   ███████╗██║  ██║
    ╚═╝  ╚═╝ ╚═════╝  ╚═════╝    ╚═╝   ╚══════╝╚═╝  ╚═╝
                                                        

    {GREEN}                                                                     
                    Verision: Beta ({sys.version[0]})
    {YELLOW}
                    Create For Education
    {END}
'''
    print(fonts)
if __name__ == '__main__':
    banner()
    debug(f'VERSION BETA PLEASE EDIT !!!\n', 'alert')
    main()
