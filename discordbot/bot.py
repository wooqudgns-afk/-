import os  # <--- 맨 위에 이거 추가하기
import discord
from discord.ext import commands, tasks
import aiohttp
import asyncio
import json
from keep_alive import keep_alive

# 봇 설정
intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

# 📌 스텔라이브 멤버 리스트
STREAMERS = [
    {
        "name": "강지",
        "chzzk_id": "b5ed5db484d04faf4d150aedd362f34b",
        "discord_channel_id": 1562750663031660634,
        "is_live": False
    },
    {
        "name": "아야츠노 유니",
        "chzzk_id": "45e71a76e949e16a34764deb962f9d9f",
        "discord_channel_id": 1562750721202585630,
        "is_live": False
    },
    {
        "name": "사키하네 후야",
        "chzzk_id": "36ddb9bb4f17593b60f1b63cec86611d",
        "discord_channel_id": 1562750735299387482,
        "is_live": False
    },
    {
        "name": "시라유키 히나",
        "chzzk_id": "b044e3a3b9259246bc92e863e7d3f3b8",
        "discord_channel_id": 1562750874881761370,
        "is_live": False
    },
    {
        "name": "네네코 마시로",
        "chzzk_id": "4515b179f86b67b4981e16190817c580",
        "discord_channel_id": 1562750817147162625,
        "is_live": False
    },
    {
        "name": "아카네 리제",
        "chzzk_id": "4325b1d5bbc321fad3042306646e2e50",
        "discord_channel_id": 1562750799111659570,
        "is_live": False
    },
    {
        "name": "아라하시 타비",
        "chzzk_id": "a6c4ddb09cdb160478996007bff35296",
        "discord_channel_id": 1562750785840742471,
        "is_live": False
    },
    {
        "name": "텐코 시부키",
        "chzzk_id": "64d76089fba26b180d9c9e48a32600d9",
        "discord_channel_id": 1562750916350705664,
        "is_live": False
    },
    {
        "name": "아오쿠모 린",
        "chzzk_id": "516937b5f85cbf2249ce31b0ad046b0f",
        "discord_channel_id": 1562750952816123965,
        "is_live": False
    },
    {
        "name": "하나코 나나",
        "chzzk_id": "4d812b586ff63f8a2946e64fa860bbf5",
        "discord_channel_id": 1562750902908092467,
        "is_live": False
    },
    {
        "name": "유즈하 리코",
        "chzzk_id": "8fd39bb8de623317de90654718638b10",
        "discord_channel_id": 1562750889150779403,
        "is_live": False
    },
    {
        "name": "시즈키 토아",
        "chzzk_id": "2299fad4bebb504b0978e1ec08b2f7d3",
        "discord_channel_id": 1562750966258733156,
        "is_live": False
    },
    {
        "name": "코가네 랑",
        "chzzk_id": "c657aa3592260a2b59669a72ec151936",
        "discord_channel_id": 1562750977436815421,
        "is_live": False
    },
    {
        "name": "하나요 히요리",
        "chzzk_id": "49d2c3cf8f0b2843d934ec15e82bb54c",
        "discord_channel_id": 1562751002489131018,
        "is_live": False
    },
    {
        "name": "토키노 메리",
        "chzzk_id": "792acf9ca28b42918710327e14b06b68",
        "discord_channel_id": 1562750987951804426,
        "is_live": False
    }
]

TOKEN = os.getenv("DISCORD_TOKEN")


async def check_chzzk_status(chzzk_id):
    """스트리머 방송 상태 및 라이브 채팅 서버(ChatChannelId)를 가져오는 함수"""
    url = f"https://api.chzzk.naver.com/service/v1/channels/{chzzk_id}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                content = data.get("content", {})
                status = content.get("openLive", False)
                live_title = content.get("liveTitle", "제목 없음")
                chat_channel_id = content.get("chatChannelId")
                return status, live_title, chat_channel_id
    return False, "", None

@tasks.loop(seconds=60)
async def live_and_chat_monitor():
    """60초마다 방송 켜짐 여부를 체크하는 루프"""
    for streamer in STREAMERS:
        channel = bot.get_channel(streamer["discord_channel_id"])
        if not channel:
            continue

        is_live, title, chat_channel_id = await check_chzzk_status(streamer["chzzk_id"])

        # 1. 방송이 방금 켜졌을 때 알림 전송
        if is_live and not streamer["is_live"]:
            streamer["is_live"] = True
            embed = discord.Embed(
                title=f"🚨 {streamer['name']} 방송 시작!",
                description=f"**{title}**",
                color=0x00FFA3
            )
            embed.add_field(name="방송국 바로가기", value=f"[클릭해서 시청하기](https://chzzk.naver.com/live/{streamer['chzzk_id']})", inline=False)
            await channel.send(embed=embed)

        # 2. 방송이 꺼졌을 때
        elif not is_live and streamer["is_live"]:
            streamer["is_live"] = False

@bot.event
async def on_ready():
    print(f"로그인 완료: {bot.user} (치지직 통합 모니터링 봇 준비 완료!)")
    live_and_chat_monitor.start()

keep_alive()
bot.run(TOKEN)