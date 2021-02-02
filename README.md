# Monitor GPU Usage

一个监控英伟达显卡占用情况的脚本，当显存剩余量达到预期值时，通知提醒。

#### 依赖

```
pip install apscheduler
pip install nvidia-ml-py3
pip install zmail
```

#### 配置

- 邮件服务器配置

  ```
  SERVER = 'xxxx@163.com'
  CODE = 'xxxxx' # 邮箱系统里的授权码
  PWD = 'xxxx' # 邮箱登录密码， 有没有都行
  ```

- 邮件客户端配置

  ```
  client_email = 'your email address'
  # 定义发送邮件的内容
  mail_content = {
      'subject': 'Success!',  # 主题
      'content_text': 'gpu is free!',
  }
  
  gpu_id = 0   # monitor GPU:0
  free_thresh = 20  # 如果0号卡有20GB显存剩余，就通知
  interval_minutes = 2  # 每2分钟检查一次显存情况
  ```

#### 运行

    ```
    nohup python main.py &
    ```
