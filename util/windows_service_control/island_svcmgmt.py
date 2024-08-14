import winrm
import time
from sys import argv
import island_cmd as cmd

try:
    param = argv[1]
except:
    param = "status"

hosts = {'im-game01-kor':'1.1.1.1'}
user_id = 'ID'
user_pw = 'PASSWORD'

def run_pwsh_cmd(pwsh_cmd):
    result_byte = session.run_ps(pwsh_cmd)
    print(result_byte.std_out.decode('utf-8'))
    return

def run_windows_cmd(windows_cmd):
    result_byte = session.run_cmd(windows_cmd)
    print(result_byte.std_out.decode('utf-8'))
    return


for hostname, ip in hosts.items():
    print(hostname, ip)
    session = winrm.Session(ip, auth=(user_id, user_pw))
    if param == 'enable_noti':
        run_pwsh_cmd(cmd.pwsh_enable_noti)
    elif param == 'disable_noti':
        run_pwsh_cmd(cmd.pwsh_disable_noti)
    elif param == 'switch_start':
        run_pwsh_cmd(cmd.pwsh_switch_start)
    elif param == 'switch_stop':
        run_pwsh_cmd(cmd.pwsh_switch_stop)
    elif param == 'switch_restart':
        run_pwsh_cmd(cmd.pwsh_switch_restart)
    elif param == 'service_start':
        run_pwsh_cmd(cmd.pwsh_service_start)
        time.sleep(1)
        run_pwsh_cmd(cmd.pwsh_service_status)
    elif param == 'service_stop':
        run_pwsh_cmd(cmd.pwsh_service_stop)
        time.sleep(1)
        run_pwsh_cmd(cmd.pwsh_service_status)
    elif param == 'service_status':
        run_pwsh_cmd(cmd.pwsh_service_status)
    elif param == 'deploy':
        run_windows_cmd(cmd.win_source_deploy)
    elif param == 'log_compress':
        run_windows_cmd(cmd.win_log_compress)
    elif param == 'gms':
        run_pwsh_cmd(cmd.pwsh_gms_stop)
        time.sleep(1)
        run_windows_cmd(cmd.gms_source_deplpoy)
        time.sleep(1)
        run_pwsh_cmd(cmd.pwsh_gms_start)
        time.sleep(1)
        run_pwsh_cmd(cmd.pwsh_gms_status)
    else:
        run_pwsh_cmd(cmd.pwsh_service_status)