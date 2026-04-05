# 飞书


## Table of Contents
- [飞书](#飞书)
  - [Table of Contents](#table-of-contents)
- [消息类型](#消息类型)
- [事件订阅](#事件订阅)
- [飞书机器人](#飞书机器人)


---

# 消息类型

message_type
1. text 文本
2. post 富文本(类似 Markdown)
3. image 图片
4. share_chat
5. interactive 交互式消息卡片


# 事件订阅

[飞书开放平台 - Website](https://open.feishu.cn/?lang=zh-CN) -> 开发者后台 -> 企业自建应用




# 飞书机器人

[Webhook - 个人笔记](../../ComputerScience/ComputerNetwork/ComputerNetwork.md#webhook)

飞书配置
1. 群聊 + 设置 + 群机器人
2. 自定义机器人 (会有 **Webhook** URL)
   1. 往 该URL 发消息，就能把消息发到群里
   2. eg : coze 完成 workflow 后 生成消息 给 webhook，robot 就把消息 发到群里
3. 事件订阅






