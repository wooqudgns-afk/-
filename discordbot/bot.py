import os
import discord
from discord.ext import commands, tasks
import aiohttp
import asyncio
import json
import feedparser  # 유튜브 RSS용 필수 도구!
from keep_alive import keep_alive

# 봇 설정
intents = discord.Intents.default()
intents.message_content = True  # 명령어 쓰려면 꼭 필요함!
bot = commands.Bot(command_prefix='!', intents=intents)

# 📌 스텔라이브 멤버 리스트 (치지직 + 유튜브 채널 ID + 채널 매칭 완료)
STREAMERS = [
    {
        "name": "강지",
        "chzzk_id": "b5ed5db484d04faf4d150aedd362f34b",
        "youtube_channel_id": "UCIVFv8AiQLqM9oLHTixrNYw",
        "discord_channel_id": 1562750663031660634,
        "is_live": False,
        "latest_youtube_id": None
    },
    {
        "name": "아야츠노 유니",
        "chzzk_id": "45e71a76e949e16a34764deb962f9d9f",
        "youtube_channel_id": "UClbYIn9LDbbFZ9w2shX3K0g",
        "discord_channel_id": 1562750721202585630,
        "is_live": False,
        "latest_youtube_id": None
    },
    {
        "name": "사키하네 후야",
        "chzzk_id": "36ddb9bb4f17593b60f1b63cec86611d",
        "youtube_channel_id": "UC0YQnenKBCu5sGb7H61n6HA",
        "discord_channel_id": 1562750735299387482,
        "is_live": False,
        "latest_youtube_id": None
    },
    {
        "name": "시라유키 히나",
        "chzzk_id": "b044e3a3b9259246bc92e863e7d3f3b8",
        "youtube_channel_id": "UC1afpiIuBDcjYlmruAa0HiA",
        "discord_channel_id": 1562750874881761370,
        "is_live": False,
        "latest_youtube_id": None
    },
    {
        "name": "네네코 마시로",
        "chzzk_id": "4515b179f86b67b4981e16190817c580",
        "youtube_channel_id": "UC_eeSpMBz8PG4ssdBPnP07g",
        "discord_channel_id": 1562750817147162625,
        "is_live": False,
        "latest_youtube_id": None
    },
    {
        "name": "아카네 리제",
        "chzzk_id": "4325b1d5bbc321fad3042306646e2e50",
        "youtube_channel_id": "UC7-m6jQLinZQWIbwm9W-1iw",
        "discord_channel_id": 1562750799111659570,
        "is_live": False,
        "latest_youtube_id": None
    },
    {
        "name": "아라하시 타비",
        "chzzk_id": "a6c4ddb09cdb160478996007bff35296",
        "youtube_channel_id": "UCAHVQ44O81aehLWfy9O6Elw",
        "discord_channel_id": 1562750785840742471,
        "is_live": False,
        "latest_youtube_id": None
    },
    {
        "name": "텐코 시부키",
        "chzzk_id": "64d76089fba26b180d9c9e48a32600d9",
        "youtube_channel_id": "UCYxLMfeX1CbMBll9MsGlzmw",
        "discord_channel_id": 1562750916350705664,
        "is_live": False,
        "latest_youtube_id": None
    },
    {
        "name": "아오쿠모 린",
        "chzzk_id": "516937b5f85cbf2249ce31b0ad046b0f",
        "youtube_channel_id": "UCQmcltnre6aG9SkDRYZqFIg",
        "discord_channel_id": 1562750952816123965,
        "is_live": False,
        "latest_youtube_id": None
    },
    {
        "name": "하나코 나나",
        "chzzk_id": "4d812b586ff63f8a2946e64fa860bbf5",
        "youtube_channel_id": "UCcA21_PzN1EhNe7xS4MJGsQ",
        "discord_channel_id": 1562750902908092467,
        "is_live": False,
        "latest_youtube_id": None
    },
    {
        "name": "유즈하 리코",
        "chzzk_id": "8fd39bb8de623317de90654718638b10",
        "youtube_channel_id": "UCj0c1jUr91dTetIQP2pFeLA",
        "discord_channel_id": 1562750889150779403,
        "is_live": False,
        "latest_youtube_id": None
    },
    {
        "name": "시즈키 토아",
        "chzzk_id": "2299fad4bebb504b0978e1ec08b2f7d3",
        "youtube_channel_id": "UClcSEuDF_g_6g4snw_nAavw",
        "discord_channel_id": 1562750966258733156,
        "is_live": False,
        "latest_youtube_id": None
    },
    {
        "name": "코가네 랑",
        "chzzk_id": "c657aa3592260a2b59669a72ec151936",
        "youtube_channel_id": "UCQ6LlsI7Bbj2yhSqLMI1gGA",
        "discord_channel_id": 1562750977436815421,
        "is_live": False,
        "latest_youtube_id": None
    },
    {
        "name": "하나요 히요리",
        "chzzk_id": "49d2c3cf8f0b2843d934ec15e82bb54c",
        "youtube_channel_id": "UCHAr9pWGS30akL4MQCQT4uQ",
        "discord_channel_id": 1562751002489131018,
        "is_live": False,
        "latest_youtube_id": None
    },
    {
        "name": "토키노 메리",
        "chzzk_id": "792acf9ca28b42918710327e14b06b68",
        "youtube_channel_id": "UCGSt1yNG5l-jpYRLpJ5oNtA",
        "discord_channel_id": 1562750987951804426,
        "is_live": False,
        "latest_youtube_id": None
    }
]

TOKEN = os.getenv("DISCORD_TOKEN")


async def check_chzzk_status(chzzk_id):
    """치지직 방송 상태 확인 함수"""
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


async def check_youtube_updates():
    """유튜브 최신 영상 확인 및 알림 함수"""
    for streamer in STREAMERS:
        yt_id = streamer.get("youtube_channel_id")
        if not yt_id:
            continue
            
        rss_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={yt_id}"
        feed = feedparser.parse(rss_url)
        
        if feed.entries:
            latest_video = feed.entries[0]
            video_id = latest_video.id.split(":")[-1]
            video_title = latest_video.title
            video_link = latest_video.link
            
            # 최초 실행 시점에는 알림을 보내지 않고 ID만 저장해 둠
            if streamer["latest_youtube_id"] is None:
                streamer["latest_youtube_id"] = video_id
            elif streamer["latest_youtube_id"] != video_id:
                streamer["latest_youtube_id"] = video_id
                channel = bot.get_channel(streamer["discord_channel_id"])
                if channel:
                    embed = discord.Embed(
                        title=f"📺 [{streamer['name']}] 새로운 유튜브 영상 업로드!",
                        description=f"**{video_title}**",
                        color=0xFF0000
                    )
                    embed.add_field(name="영상 보러 가기", value=f"[클릭해서 시청하기]({video_link})", inline=False)
                    await channel.send(embed=embed)


@tasks.loop(seconds=60)
async def live_and_chat_monitor():
    """60초마다 치지직 생방송 + 유튜브 업로드를 동시에 체크하는 루프"""
    # 1. 치지직 생방송 체크
    for streamer in STREAMERS:
        channel = bot.get_channel(streamer["discord_channel_id"])
        if not channel:
            continue

        is_live, title, chat_channel_id = await check_chzzk_status(streamer["chzzk_id"])

        # 방송 시작 알림
        if is_live and not streamer["is_live"]:
            streamer["is_live"] = True
            embed = discord.Embed(
                title=f"🚨 {streamer['name']} 방송 시작!",
                description=f"**{title}**",
                color=0x00FFA3
            )
            embed.add_field(name="방송국 바로가기", value=f"[클릭해서 시청하기](https://chzzk.naver.com/live/{streamer['chzzk_id']})", inline=False)
            await channel.send(embed=embed)

        # 방송 종료
        elif not is_live and streamer["is_live"]:
            streamer["is_live"] = False

    # 2. 유튜브 업로드 체크
    await check_youtube_updates()


# 수동 테스트 명령어 추가! (!알림테스트 강지)
@bot.command(name="알림테스트")
async def test_alert(ctx, *, streamer_name: str):
    target = None
    for s in STREAMERS:
        if s["name"] == streamer_name:
            target = s
            break
            
    if not target:
        await ctx.send(f"❌ '{streamer_name}' 스트리머를 찾을 수 없어! 이름을 다시 확인해 봐.")
        return

    await ctx.send(f"🔍 '{streamer_name}'의 방송 상태를 확인하는 중...")
    is_live, title, _ = await check_chzzk_status(target["chzzk_id"])
    
    if is_live:
        embed = discord.Embed(
            title=f"🚨 [테스트] {target['name']} 방송 중!",
            description=f"**{title}**",
            color=0x00FFA3
        )
        embed.add_field(name="방송국 바로가기", value=f"[클릭해서 시청하기](https://chzzk.naver.com/live/{target['chzzk_id']})", inline=False)
        await ctx.send(embed=embed)
    else:
        await ctx.send(f"💤 현재 **{target['name']}**님은 방송 꺼져 있는 상태야! (오프라인)")


@bot.event
async def on_ready():
    print(f"로그인 완료: {bot.user} (스텔라이브 통합 알림 봇 준비 완료!)")
    if not live_and_chat_monitor.is_running():
        live_and_chat_monitor.start()


if __name__ == "__main__":
    keep_alive()  # 렌더 안 꺼지게 웹서버 먼저 켜고
    bot.run(TOKEN) # 봇 실행