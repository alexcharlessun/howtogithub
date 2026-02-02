from typing import Any
import asyncio
import psutil
from mcp.server.fastmcp import FastMCP

# 初始化一个名为 "System Monitor" 的 MCP 服务器
mcp = FastMCP("System Monitor")

# ==============================================================================
# Resource (资源): 就像是一个只读的文件或数据源
# 当 AI 需要知道 "系统状态" 时，它会读取这个资源
# ==============================================================================
@mcp.resource("system://stats")
def get_system_stats() -> str:
    """获取当前系统的 CPU 和内存使用率"""
    cpu_percent = psutil.cpu_percent(interval=0.1)
    memory = psutil.virtual_memory()
    
    # 返回 JSON 风格的字符串（或者直接是一段描述性文本）
    return f'{{"cpu_percent": {cpu_percent}, "memory_percent": {memory.percent}}}'

# ==============================================================================
# Tool (工具): 就像是一个函数，AI 可以主动调用它来执行动作或查询复杂数据
# 当 AI 需要 "查谁占了内存" 时，它会调用这个工具
# ==============================================================================
@mcp.tool()
def list_top_processes(sort_by: str = "memory", limit: int = 5) -> str:
    """
    列出资源占用最高的进程。
    
    Args:
        sort_by: 排序方式，可选 "memory" (内存) 或 "cpu" (CPU)
        limit: 返回的进程数量，默认为 5
    """
    # 确定排序的字段
    sort_key = "memory_percent" if sort_by == "memory" else "cpu_percent"
    
    processes = []
    # 遍历所有运行中的进程
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            p_info = proc.info
            # 有些进程可能无法访问，跳过即可
            if p_info:
                processes.append(p_info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    # 排序并取前 N 个
    sorted_procs = sorted(processes, key=lambda p: p[sort_key] or 0, reverse=True)[:limit]
    
    # 为了让 AI 容易读懂，我们格式化成简单的文本列表
    result_lines = [f"Top {limit} processes by {sort_by}:"]
    for p in sorted_procs:
        cpu = p['cpu_percent']
        mem = p['memory_percent']
        result_lines.append(f"- [{p['pid']}] {p['name']}: CPU {cpu}%, Mem {mem:.1f}%")
        
    return "\n".join(result_lines)

if __name__ == "__main__":
    # 以标准输入/输出 (stdio) 模式运行服务器
    # 这是本地 MCP 通信的标准方式
    mcp.run()
