from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import asyncio
import sys

async def run():
    # 配置要连接的服务器参数
    server_params = StdioServerParameters(
        command=sys.executable,  # 使用当前运行环境的 python (即虚拟环境内的 python)
        args=["system_monitor_mcp/server.py"], # 指定运行我们的 server 脚本
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # 1. 初始化连接
            await session.initialize()
            print("\n✅ Connected to MCP Server!")

            # 2. 列出所有资源
            resources = await session.list_resources()
            print(f"\n📂 Found {len(resources.resources)} Resources:")
            for res in resources.resources:
                print(f" - {res.name} ({res.uri})")

            # 3. 读取 system://stats 资源
            print(f"\n📖 Reading resource 'system://stats'...")
            try:
                content = await session.read_resource("system://stats")
                # content 是一个列表，每一项有 text 或 blob
                print(f"Content: {content.contents[0].text}")
            except Exception as e:
                print(f"Error reading resource: {e}")

            # 4. 列出所有工具
            tools = await session.list_tools()
            print(f"\n🛠️ Found {len(tools.tools)} Tools:")
            for tool in tools.tools:
                print(f" - {tool.name}: {tool.description}")

            # 5. 调用 list_top_processes 工具
            print(f"\n🚀 Invoking tool 'list_top_processes'...")
            try:
                result = await session.call_tool("list_top_processes", arguments={"limit": 3})
                # result.content 是个列表
                print(f"Result:\n{result.content[0].text}")
            except Exception as e:
                print(f"Error calling tool: {e}")

if __name__ == "__main__":
    asyncio.run(run())
