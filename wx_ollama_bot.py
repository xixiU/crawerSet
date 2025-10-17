import itchat
import requests
from itchat.content import TEXT
from typing import Optional

class OllamaBot:
    def __init__(self, ollama_url: str = "http://116.62.116.255:11434"):
        self.ollama_url = ollama_url
        self.model = "deepseek-r1:70b-c8k"  # 默认使用mistral模型，你也可以换成其他模型
        
    def get_response(self, prompt: str) -> Optional[str]:
        """调用Ollama API获取回复"""
        try:
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False
                }
            )
            if response.status_code == 200:
                return response.json()["response"]
            return None
        except Exception as e:
            print(f"调用Ollama API时出错: {str(e)}")
            return None

# 初始化机器人
bot = OllamaBot()

@itchat.msg_register(TEXT)
def handle_text_message(msg):
    """处理接收到的文本消息"""
    # 获取消息内容
    content = msg['Content']
    
    # 检查消息是否以"回答本王"开头
    if content.startswith("回答本王"):
        # 提取问题内容
        question = content[4:].strip()
        
        # 获取回复
        response = bot.get_response(question)
        
        # 如果成功获取回复，则发送
        if response:
            # 判断消息来源
            if msg['FromUserName'] == msg['ToUserName']:
                # 私聊消息
                return response
            else:
                # 群聊消息，@发送者
                return f"@{msg['ActualNickName']}\n{response}"
        else:
            return "抱歉，我现在无法回答这个问题。"

def main():
    # 登录微信
    itchat.auto_login(enableCmdQR=2)
    print("微信机器人已启动...")
    
    # 运行机器人
    itchat.run()

# if __name__ == "__main__":
#     main() 

def get_step(m: int, n: int) -> int:
    """
    计算从m到n的最少步数
    :param m: 起始数字
    :param n: 目标数字
    :return: 最少步数，如果无法到达则返回-1
    """
    if m >= n:
        return -1
    
    # 使用集合记录已访问的数字，避免重复计算
    visited = set()
    # 队列存储(当前数字，步数)
    queue = [(m, 0)]
    
    while queue:
        curr_num, steps = queue.pop(0)
        
        # 检查是否达到目标
        if curr_num == n:
            return steps
            
        # 尝试两种操作
        operations = [curr_num * 2, curr_num - 1]
        for next_num in operations:
            # 确保数字在有效范围内且未被访问过
            if 0 < next_num <= n and next_num not in visited:
                visited.add(next_num)
                queue.append((next_num, steps + 1))
    
    return -1

print(get_step(1,10))
print(get_step(3,10))
print(get_step(4,10))
print(get_step(3,4))

