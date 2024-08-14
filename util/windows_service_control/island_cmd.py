pwsh_service_start = '''
[string[]]$params_service =
    "IslandM.ChattingServer",
    "IslandM.GameServer",
    "IslandM.MoServer",
    "IslandM.Filebeat"
Start-Service $params_service
'''

pwsh_service_stop = '''
[string[]]$params_service =
    "IslandM.Filebeat",
    "IslandM.ChattingServer",
    "IslandM.GameServer",
    "IslandM.MoServer"
Stop-Service $params_service
'''

pwsh_switch_start = '''
[string[]]$params_service = "IslandM.SwitchServer"
Start-Service $params_service
'''

pwsh_switch_stop = '''
[string[]]$params_service = "IslandM.SwitchServer"
Stop-Service $params_service
'''

pwsh_switch_restart = '''
[string[]]$params_service = "IslandM.SwitchServer"
restart-Service $params_service
'''

pwsh_enable_noti = '''
$ItemPath = "E:\IslandM\Servers\Switch\Versions.cfg"
$Text = Get-Content $ItemPath
$EnableNoti = @"
"Notification":"/Image/noti/maintenance.jpg","LinkUrl":"https://m.cafe.naver.com/""
"@
$DisableNoti = @"
"Notification":"","LinkUrl":""
"@
$Text.replace($DisableNoti, $EnableNoti)|Set-Content $ItemPath
'''

pwsh_disable_noti = '''
$ItemPath = "E:\IslandM\Servers\Switch\Versions.cfg"
$Text = Get-Content $ItemPath
$EnableNoti = @"
"Notification":"/Image/noti/maintenance.jpg","LinkUrl":"https://m.cafe.naver.com/""
"@
$DisableNoti = @"
"Notification":"","LinkUrl":""
"@
$Text.replace($EnableNoti, $DisableNoti)|Set-Content $ItemPath
'''

pwsh_service_status = 'Get-Service IslandM*'

pwsh_gms_start = '''
Start-IISSite -Name "GMS"
'''

pwsh_gms_stop = '''
Stop-IISSite -Name "GMS"
'''

pwsh_gms_status = '''
Get-IISSite -Name "GMS"
'''

win_source_deploy = '''
rsync -ave 'ssh -o "StrictHostKeyChecking no" -i /cygdrive/e/gamepub/sshkey/island_deploy' \
--delete \
--exclude="Log" \
devgame@10.0.0.10:/cygdrive/f/islandm/servers_live/* /cygdrive/e/islandm/servers/
'''

gms_source_deplopy = '''
rsync -ave 'ssh -o "StrictHostKeyChecking no" -i /cygdrive/islandm/authkey/island_deploy' \
--exclude="Web.config" \
devgame@10.0.0.4:/cygdrive/c/GMS/* /cygdrive/e/GMS/
'''

win_log_compress = '''
e:\gamepub\cygwin\find /cygdrive/e/islandm/servers -type f -name "*.log" -mtime +2 |xargs gzip -v
'''