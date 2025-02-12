# OASIS 用户管理工具

这是一个用于H3C OASIS系统的用户管理工具，可以帮助管理员快速创建新用户账号。

## 功能特点

- 支持创建新用户账号
- 自定义用户信息配置
- 自动化HTTP请求处理

## 使用说明

### 必要参数

- `owner_name`: 所有者名称
- `user_name`: 用户名
- `user_password`: 用户密码
- `store_id`: 商店ID
- `user_email`: 用户邮箱
- `phone_no`: 电话号码
- `expire_time`: 账号过期时间
- `remark`: 备注信息
- `send_email`: 是否发送邮件通知

### 可选参数

- `incar`: 入场车牌号(默认为None)
- `outcar`: 出场车牌号(默认为None)
- `onlineMaxTime`: 最大在线时间(默认为None)
- `dayMaxTime`: 每日最大使用时间(默认为None)
- `idleCutTime`: 空闲切断时间(默认为None)
- `idleCutFlow`: 空闲流量限制(默认为None)

## 使用示例

```python
# 创建新用户示例
user_info = {
    "owner_name": "test",
    "user_name": "test_user",
    "user_password": "password123",
    "store_id": "1001",
    "user_email": "test@example.com",
    "phone_no": "13800138000",
    "expire_time": "2024-12-31",
    "remark": "测试用户",
    "send_email": False
}

# 调用接口创建用户
response = create_user(**user_info)

## env环境
.env 文件内需包含从浏览器获取的cookie信息：COOKIE="connect.sid=XXXXXXXX*cas.login"   