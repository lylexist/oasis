import requests
import json
import pandas as pd
from tqdm import tqdm
import time
import logging
import os

#引入dotenv
from dotenv import load_dotenv

# 加载.env文件中的环境变量
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)
COOKIE = os.getenv('COOKIE')

# 设置日志
logging.basicConfig(filename='user_addition.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')


def add_user(owner_name, user_name, user_password, store_id, user_email="", phone_no="", remark="", send_email=0, expire_time=0):
    url = "https://oasis.h3c.com/v3/ace/oasis/auth-data/o2oportal/registuser/add"
    
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en,zh-CN;q=0.9,zh;q=0.8,zh-TW;q=0.7",
        "cache-control": "no-cache",
        "content-type": "application/json;charset=UTF-8",
        "cookie": COOKIE,
        "origin": "https://oasis.h3c.com",
        "pragma": "no-cache",
        "referer": "https://oasis.h3c.com/oasis6/static/",
        "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    }
    
    data = {
        "ownerName": owner_name,
        "userName": user_name,
        "userPassword": user_password,
        "passwordConfirm": user_password,
        "storeId": store_id,
        "userEmail": user_email,
        "phoneNo": phone_no,
        "remark": remark,
        "sendEmail": send_email,
        "incar": None,
        "outcar": None,
        "onlineMaxTime": None,
        "dayMaxTime": None,
        "idleCutTime": None,
        "idleCutFlow": None,
        "ugName": "",
        "expireTime": expire_time,
        "macBindList": []
    }
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        response_data = response.json()
        
        if response_data.get('errorcode') == 0:
            return True, "用户添加成功", response_data
        else:
            return False, f"用户添加失败: errorcode = {response_data.get('errorcode')}", response_data
    except requests.RequestException as e:
        return False, f"请求失败: {str(e)}", None

def process_excel_data(file_path, owner_name, store_id, batch_size=100):
    # 读取Excel文件，跳过前3行
    df = pd.read_excel(file_path, skiprows=3, usecols=[0, 1, 6], names=['user_name', 'user_password', 'remark'])
    
    total_users = len(df)
    successful_additions = 0
    failed_additions = 0

    for i in tqdm(range(0, total_users, batch_size), desc="处理批次"):
        batch = df.iloc[i:i+batch_size]
        for _, row in batch.iterrows():
            success, message, data = add_user(
                owner_name=owner_name,
                user_name=row['user_name'],
                user_password=row['user_password'],
                store_id=store_id,
                remark=row['remark']
            )
            if success:
                successful_additions += 1
                logging.info(f"成功添加用户: {row['user_name']}")
            else:
                failed_additions += 1
                logging.error(f"添加用户失败: {row['user_name']} - {message}")
            
            # 添加短暂延迟以避免请求过于频繁
            time.sleep(0.1)
        
        # 每批次后打印进度
        print(f"已处理 {min(i+batch_size, total_users)}/{total_users} 用户")

    print(f"\n处理完成！成功添加: {successful_additions}, 失败: {failed_additions}")
    logging.info(f"处理完成！成功添加: {successful_additions}, 失败: {failed_additions}")

# 使用示例
if __name__ == "__main__":
    excel_file_path = "account.xlsx"  # 请替换为实际的Excel文件路径
    owner_name = "xxxxxx"  # 请替换为实际的owner_name
    store_id = 1234567  # 请替换为实际的store_id
    
    #process_excel_data(excel_file_path, owner_name, store_id)
    success, message, data = add_user(

        owner_name=owner_name, 
        store_id=store_id,
        user_name='test223',
        user_password='123456.com', 
        remark='测试用户'
    )
    
    if success:
        logging.info(f"成功添加用户")


    else:
        logging.error(f"添加用户失败: {message}")


