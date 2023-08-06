# ifttt手机通知发送SDK

官方网站:[https://ifttt.com/if_notifications](https://ifttt.com/if_notifications)

# DEMO
```
#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from ifttt import notice

text = '服务器1号:任务完成'
response = notice.send_notice(event_name='test', key='dXGc1k52h7GflYU4Lcjt7G', text=text)
print(response)
```