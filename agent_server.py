from fastapi import FastAPI
import pymysql
import openai
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI()

# 跨域配置（必须保留，解决前端跨域）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========== 1. 阿里云百炼核心配置 ==========
# 替换为你自己的有效 API Key（从阿里百炼控制台获取）
ALIYUN_API_KEY = "sk-a9501c814bbd44b4b76b2c5a936fa594"
ALIYUN_BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
LLM_MODEL = "qwen-turbo"  # 免费版，稳定可用

# 初始化 OpenAI 兼容客户端（对接阿里百炼）
client = openai.OpenAI(
    api_key=ALIYUN_API_KEY,
    base_url=ALIYUN_BASE_URL
)

# ========== 2. 数据库配置（你的人事系统）==========
DB_HOST = "localhost"
DB_USER = "root"
DB_PWD = "2003"
DB_NAME = "personmis"

def get_db_connection():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PWD,
        database=DB_NAME,
        charset="utf8"
    )

# ========== 3. 数据库工具函数（岗位查询）==========
def query_post_count(post_type: str) -> str:
    """查询指定类型岗位数量"""
    try:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("SELECT COUNT(*) FROM post WHERE ptype = %s", (post_type,))
        count = cursor.fetchone()[0]
        db.close()
        return f"「{post_type}」类型岗位数量：{count} 个"
    except Exception as e:
        return f"查询岗位数量失败：{str(e)}"

def query_post_organization_sum(post_type: str = None) -> str:
    """统计岗位编制人数总和"""
    try:
        db = get_db_connection()
        cursor = db.cursor()
        if post_type:
            cursor.execute("SELECT SUM(organization) FROM post WHERE ptype = %s", (post_type,))
        else:
            cursor.execute("SELECT SUM(organization) FROM post")
        total = cursor.fetchone()[0] or 0
        db.close()
        if post_type:
            return f"「{post_type}」类型岗位编制人数总和：{total} 人"
        else:
            return f"所有岗位编制人数总和：{total} 人"
    except Exception as e:
        return f"统计编制人数失败：{str(e)}"

# ========== 4. 大模型工具定义（Function Call）==========
tools = [
    {
        "type": "function",
        "function": {
            "name": "query_post_count",
            "description": "查询指定类型的岗位数量，输入参数是岗位类型（如：技术、营销、管理）",
            "parameters": {
                "type": "object",
                "properties": {
                    "post_type": {
                        "type": "string",
                        "description": "岗位类型，例如：技术、管理、营销、财务等"
                    }
                },
                "required": ["post_type"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "query_post_organization_sum",
            "description": "统计岗位编制人数总和，可指定岗位类型（可选参数），不指定则统计所有岗位",
            "parameters": {
                "type": "object",
                "properties": {
                    "post_type": {
                        "type": "string",
                        "description": "岗位类型（可选），例如：技术、管理、营销等"
                    }
                }
            }
        }
    }
]

tool_map = {
    "query_post_count": query_post_count,
    "query_post_organization_sum": query_post_organization_sum
}

# ========== 5. 核心接口：自由聊天 + 智能调用工具 ==========
@app.post("/api/hr/agent/query")
def agent_query(data: dict):
    user_query = data.get("user_query", "").strip()
    employee_id = data.get("employee_id", "")

    if not user_query:
        return {"success": False, "answer": "请输入你的问题"}

    try:
        # Step 1: 向百炼大模型发送初始请求
        messages = [
            {
                "role": "system",
                "content": """你是人事管理智能助手，既可以回答岗位相关的专业问题，也可以进行日常聊天。
                当用户询问岗位数量、编制等需要查询数据库的问题时，你必须调用提供的工具函数，禁止编造数据。
                当用户进行日常聊天或询问通用知识时，你可以直接回答，无需调用工具。
                工具调用后，根据返回结果整理成自然语言回答用户。 当用户问“有多少个岗位”时，调用 `query_post_count`。
                当用户问“有多少人”、“总人数”、“编制人数”时，调用 `query_post_organization_sum`。
                禁止混淆这两个概念，禁止编造数据。"""
            },
            {"role": "user", "content": user_query}
        ]

        # 调用阿里百炼大模型
        response = client.chat.completions.create(
            model=LLM_MODEL,
            messages=messages,
            tools=tools,
            tool_choice="auto",  # 自动判断是否调用工具
            temperature=0.7       # 0.7 兼顾准确性和自然度，适合聊天
        )

        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls

        # Step 2: 如果需要调用工具，执行数据库查询
        if tool_calls:
            messages.append(response_message)

            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_to_call = tool_map.get(function_name)
                
                if not function_to_call:
                    continue

                # 安全解析参数
                function_args = json.loads(tool_call.function.arguments)
                # 执行工具函数
                function_response = function_to_call(**function_args)

                # 将工具结果返回给大模型
                messages.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                })

            # Step 3: 再次调用大模型，整理结果为自然语言
            second_response = client.chat.completions.create(
                model=LLM_MODEL,
                messages=messages
            )
            final_answer = second_response.choices[0].message.content
        else:
            # 无需调用工具，直接返回大模型回答
            final_answer = response_message.content

        return {"success": True, "answer": final_answer}

    except Exception as e:
        error_info = f"服务端错误：{str(e)}"
        print(error_info)
        return {"success": False, "answer": error_info}

# ========== 启动服务 ==========
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)