import os
import discord
from discord.ext import commands, tasks
import aiohttp
import feedparser
from datetime import datetime
from keep_alive import keep_alive

# 봇 설정
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# 📌 스텔라이브 멤버 리스트 (실제 생일 및 데뷔일 적용 완료!)
STREAMERS = [
    {
        "name": "스텔라이브",
        "youtube_channel_id": "UC2b4WRE5BZ6SIUWBeJU8rwg",
        "twitter_username": "StelLive_kr",
        "birthday": "2022-06-25",
        "debut": "2022-12-19",
        "discord_channel_id": 1562773780823281714,
        "is_live": False,
        "latest_youtube_id": None,
        "latest_tweet_id": None,
        "last_anniversary_check": None
    },
    {
        "name": "강지",
        "chzzk_id": "b5ed5db484d04faf4d150aedd362f34b",
        "youtube_channel_id": "UCIVFv8AiQLqM9oLHTixrNYw",
        "twitter_username": "GANGZIIII",
        "birthday": "1997-05-14",
        "debut": "2018-01-01",
        "discord_channel_id": 1562750663031660634,
        "is_live": False,
        "latest_youtube_id": None,
        "latest_tweet_id": None,
        "last_anniversary_check": None
    },
    {
        "name": "유니",
        "chzzk_id": "45e71a76e949e16a34764deb962f9d9f",
        "youtube_channel_id": "UClbYIn9LDbbFZ9w2shX3K0g",
        "twitter_username": "AyatsunoYuni",
        "birthday": "2023-05-21",
        "debut": "2023-01-08",
        "discord_channel_id": 1562750721202585630,
        "is_live": False,
        "latest_youtube_id": None,
        "latest_tweet_id": None,
        "last_anniversary_check": None
    },
    {
        "name": "후야",
        "chzzk_id": "36ddb9bb4f17593b60f1b63cec86611d",
        "youtube_channel_id": "UC0YQnenKBCu5sGb7H61n6HA",
        "twitter_username": "SakihaneHuya",
        "birthday": "2025-07-07",
        "debut": "2025-09-20",
        "discord_channel_id": 1562750735299387482,
        "is_live": False,
        "latest_youtube_id": None,
        "latest_tweet_id": None,
        "last_anniversary_check": None
    },
    {
        "name": "히나",
        "chzzk_id": "b044e3a3b9259246bc92e863e7d3f3b8",
        "youtube_channel_id": "UC1afpiIuBDcjYlmruAa0HiA",
        "twitter_username": "Shirayukihina_",
        "birthday": "2023-01-05",
        "debut": "2023-06-10",
        "discord_channel_id": 1562750874881761370,
        "is_live": False,
        "latest_youtube_id": None,
        "latest_tweet_id": None,
        "last_anniversary_check": None
    },
    {
        "name": "시로",
        "chzzk_id": "4515b179f86b67b4981e16190817c580",
        "youtube_channel_id": "UC_eeSpMBz8PG4ssdBPnP07g",
        "twitter_username": "NenekoMashiro",
        "birthday": "2023-02-22",
        "debut": "2023-06-10",
        "discord_channel_id": 1562750817147162625,
        "is_live": False,
        "latest_youtube_id": None,
        "latest_tweet_id": None,
        "last_anniversary_check": None
    },
    {
        "name": "리제",
        "chzzk_id": "4325b1d5bbc321fad3042306646e2e50",
        "youtube_channel_id": "UC7-m6jQLinZQWIbwm9W-1iw",
        "twitter_username": "AkaneLize",
        "birthday": "2023-10-01",
        "debut": "2023-06-11",
        "discord_channel_id": 1562750799111659570,
        "is_live": False,
        "latest_youtube_id": None,
        "latest_tweet_id": None,
        "last_anniversary_check": None
    },
    {
        "name": "타비",
        "chzzk_id": "a6c4ddb09cdb160478996007bff35296",
        "youtube_channel_id": "UCAHVQ44O81aehLWfy9O6Elw",
        "twitter_username": "ArahashiTabi",
        "birthday": "2023-09-07",
        "debut": "2023-06-11",
        "discord_channel_id": 1562750785840742471,
        "is_live": False,
        "latest_youtube_id": None,
        "latest_tweet_id": None,
        "last_anniversary_check": None
    },
    {
        "name": "부키",
        "chzzk_id": "64d76089fba26b180d9c9e48a32600d9",
        "youtube_channel_id": "UCYxLMfeX1CbMBll9MsGlzmw",
        "twitter_username": "TenkoShibuki",
        "birthday": "2024-03-21",
        "debut": "2024-05-18",
        "discord_channel_id": 1562750916350705664,
        "is_live": False,
        "latest_youtube_id": None,
        "latest_tweet_id": None,
        "last_anniversary_check": None
    },
    {
        "name": "린",
        "chzzk_id": "516937b5f85cbf2249ce31b0ad046b0f",
        "youtube_channel_id": "UCQmcltnre6aG9SkDRYZqFIg",
        "twitter_username": "AokumoRin",
        "birthday": "2024-05-03",
        "debut": "2024-05-18",
        "discord_channel_id": 1562750952816123965,
        "is_live": False,
        "latest_youtube_id": None,
        "latest_tweet_id": None,
        "last_anniversary_check": None
    },
    {
        "name": "나나",
        "chzzk_id": "4d812b586ff63f8a2946e64fa860bbf5",
        "youtube_channel_id": "UCcA21_PzN1EhNe7xS4MJGsQ",
        "twitter_username": "HanakoNana_",
        "birthday": "2024-08-07",
        "debut": "2024-05-19",
        "discord_channel_id": 1562750902908092467,
        "is_live": False,
        "latest_youtube_id": None,
        "latest_tweet_id": None,
        "last_anniversary_check": None
    },
    {
        "name": "리코",
        "chzzk_id": "8fd39bb8de623317de90654718638b10",
        "youtube_channel_id": "UCj0c1jUr91dTetIQP2pFeLA",
        "twitter_username": "YuzuhaRiko",
        "birthday": "2024-04-13",
        "debut": "2024-05-19",
        "discord_channel_id": 1562750889150779403,
        "is_live": False,
        "latest_youtube_id": None,
        "latest_tweet_id": None,
        "last_anniversary_check": None
    },
    {
        "name": "토아",
        "chzzk_id": "2299fad4bebb504b0978e1ec08b2f7d3",
        "youtube_channel_id": "UClcSEuDF_g_6g4snw_nAavw",
        "twitter_username": "ShizukiToa_",
        "birthday": "2026-11-22",
        "debut": "2026-10-17",
        "discord_channel_id": 1562750966258733156,
        "is_live": False,
        "latest_youtube_id": None,
        "latest_tweet_id": None,
        "last_anniversary_check": None
    },
    {
        "name": "랑",
        "chzzk_id": "c657aa3592260a2b59669a72ec151936",
        "youtube_channel_id": "UCQ6LlsI7Bbj2yhSqLMI1gGA",
        "twitter_username": "CoganeRang",
        "birthday": "2026-08-22",
        "debut": "2026-10-17",
        "discord_channel_id": 1562750977436815421,
        "is_live": False,
        "latest_youtube_id": None,
        "latest_tweet_id": None,
        "last_anniversary_check": None
    },
    {
        "name": "요리",
        "chzzk_id": "49d2c3cf8f0b2843d934ec15e82bb54c",
        "youtube_channel_id": "UCHAr9pWGS30akL4MQCQT4uQ",
        "twitter_username": "HanayoHiyori",
        "birthday": "2026-03-31",
        "debut": "2026-10-18",
        "discord_channel_id": 1562751002489131018,
        "is_live": False,
        "latest_youtube_id": None,
        "latest_tweet_id": None,
        "last_anniversary_check": None
    },
    {
        "name": "메리",
        "chzzk_id": "792acf9ca28b42918710327e14b06b68",
        "youtube_channel_id": "UCGSt1yNG5l-jpYRLpJ5oNtA",
        "twitter_username": "TokinoMary",
        "birthday": "2026-06-13",
        "debut": "2026-10-18",
        "discord_channel_id": 1562750987951804426,
        "is_live": False,
        "latest_youtube_id": None,
        "latest_tweet_id": None,
        "last_anniversary_check": None
    }
]

TOKEN = os.getenv("DISCORD_TOKEN")


async def check_chzzk_status(chzzk_id):
    """치지직 방송 상태 및 프로필 이미지 확인 함수"""
    url = f"https://api.chzzk.naver.com/service/v1/channels/{chzzk_id}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        timeout = aiohttp.ClientTimeout(total=5)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    print("치지직 API 응답 데이터:", data)  # 👈 이 줄을 추가!
                    content = data.get("content", {})
                    status = content.get("openLive", False)
                    live_title = content.get("liveTitle", "제목 없음")
                    chat_channel_id = content.get("chatChannelId")
                    profile_image = content.get("imageUrl", "")
                    return status, live_title, chat_channel_id, profile_image
    except Exception as e:
        print(f"치지직 API 호출 에러 ({chzzk_id}): {e}")
    
    return False, "", None, ""


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


async def check_twitter_updates():
    """X(트위터) 최신 글 확인 및 알림 함수"""
    for streamer in STREAMERS:
        twt_user = streamer.get("twitter_username")
        if not twt_user:
            continue
            
        rss_url = f"https://nitter.poast.org/{twt_user}/rss"
        feed = feedparser.parse(rss_url)
        
        if feed.entries:
            latest_tweet = feed.entries[0]
            tweet_id = latest_tweet.id
            tweet_content = latest_tweet.title
            tweet_link = latest_tweet.link
            
            if streamer["latest_tweet_id"] is None:
                streamer["latest_tweet_id"] = tweet_id
            elif streamer["latest_tweet_id"] != tweet_id:
                streamer["latest_tweet_id"] = tweet_id
                channel = bot.get_channel(streamer["discord_channel_id"])
                if channel:
                    embed = discord.Embed(
                        title=f"🐦 [{streamer['name']}] 새로운 X(트위터) 게시글!",
                        description=f"{tweet_content[:200]}...",
                        color=0x1DA1F2
                    )
                    embed.add_field(name="원문 보러 가기", value=f"[트윗 보러 가기]({tweet_link})", inline=False)
                    await channel.send(embed=embed)


async def check_anniversaries():
    """생일 및 데뷔일 기념일 체크 함수"""
    now = datetime.now()
    today_str = now.strftime("%Y-%m-%d")
    today_md = now.strftime("%m-%d")
    
    for streamer in STREAMERS:
        channel = bot.get_channel(streamer["discord_channel_id"])
        if not channel:
            continue
            
        if streamer.get("last_anniversary_check") == today_str:
            continue
            
        bday_str = streamer.get("birthday")
        debut_str = streamer.get("debut")
        
        if bday_str and bday_str[5:] == today_md:
            streamer["last_anniversary_check"] = today_str
            birth_year = int(bday_str[:4])
            current_age_years = now.year - birth_year
            
            embed = discord.Embed(
                title=f"🎂 오늘은 [{streamer['name']}]의 생일입니다!",
                description=f"다 함께 {streamer['name']}님의 **{current_age_years}번째 생일**을 축하해 주세요! 🎉✨",
                color=0xFF69B4
            )
            await channel.send(embed=embed)
            
        if debut_str and debut_str[5:] == today_md:
            streamer["last_anniversary_check"] = today_str
            debut_date = datetime.strptime(debut_str, "%Y-%m-%d")
            years_passed = now.year - debut_date.year
            
            if years_passed > 0:
                desc = f"벌써 감격스러운 **데뷔 {years_passed}주년**이에요! 앞으로도 오래오래 함께해요 💖"
            else:
                desc = f"데뷔 기념일이에요! 🎉"
                
            embed = discord.Embed(
                title=f"🎊 오늘은 [{streamer['name']}]의 데뷔 기념일!",
                description=desc,
                color=0xFFD700
            )
            await channel.send(embed=embed)
            
        if debut_str:
            debut_date = datetime.strptime(debut_str, "%Y-%m-%d")
            delta = datetime.now() - debut_date
            days_passed = delta.days + 1
            
            if days_passed > 0 and (days_passed % 100 == 0 or days_passed == 50):
                check_key = f"day_{days_passed}"
                if streamer.get("last_anniversary_check") != check_key:
                    streamer["last_anniversary_check"] = check_key
                    embed = discord.Embed(
                        title=f"✨ [{streamer['name']}] 데뷔 {days_passed}일째!",
                        description=f"오늘은 {streamer['name']}님이 세상에 빛을 보인 지 **{days_passed}일**째 되는 날이에요! 🥳",
                        color=0x00BFFF
                    )
                    await channel.send(embed=embed)


@tasks.loop(seconds=60)
async def live_and_chat_monitor():
    for streamer in STREAMERS:
        if not streamer.get("chzzk_id"):
            continue
            
        channel = bot.get_channel(streamer["discord_channel_id"])
        if not channel:
            continue

        is_live, title, chat_channel_id, profile_image = await check_chzzk_status(streamer["chzzk_id"])

        if is_live and not streamer["is_live"]:
            streamer["is_live"] = True
            embed = discord.Embed(
                title=f"🚨 {streamer['name']} 방송 시작!",
                description=f"**{title}**",
                color=0x00FFA3
            )
            embed.add_field(name="방송국 바로가기", value=f"[클릭해서 시청하기](https://chzzk.naver.com/live/{streamer['chzzk_id']})", inline=False)
            
            # 🖼️ 프로필 사진 썸네일 적용
            if profile_image:
                embed.set_thumbnail(url=profile_image)
                
            await channel.send(embed=embed)

        elif not is_live and streamer["is_live"]:
            streamer["is_live"] = False

    await check_youtube_updates()
    await check_twitter_updates()
    await check_anniversaries()


@bot.command(name="알림테스트")
async def test_alert(ctx, *, streamer_name: str):
    target = None
    for s in STREAMERS:
        if s["name"] == streamer_name:
            target = s
            break
            
    if not target:
        await ctx.send(f"❌ '{streamer_name}' 스트리머를 찾을 수 없어!")
        return

    if not target.get("chzzk_id"):
        await ctx.send(f"ℹ️ '{target['name']}'은(는) 치지직 생방송 채널이 없는 공식 계정이야!")
        return

    await ctx.send(f"🔍 '{streamer_name}'의 방송 상태를 확인하는 중...")
    is_live, title, _, profile_image = await check_chzzk_status(target["chzzk_id"])
    
    if is_live:
        embed = discord.Embed(
            title=f"🚨 [테스트] {target['name']} 방송 중!",
            description=f"**{title}**",
            color=0x00FFA3
        )
        embed.add_field(name="방송국 바로가기", value=f"[클릭해서 시청하기](https://chzzk.naver.com/live/{target['chzzk_id']})", inline=False)
        if profile_image:
            embed.set_thumbnail(url=profile_image)
        await ctx.send(embed=embed)
    else:
        await ctx.send(f"💤 현재 **{target['name']}**님은 방송 꺼져 있는 상태야!")


@bot.event
async def on_ready():
    print(f"로그인 완료: {bot.user}")
    
    # 🔄 재시작 시 이미 켜져 있는 방송은 알림 스킵하도록 상태 동기화
    print("🔍 현재 방송 상태 동기화 중...")
    for streamer in STREAMERS:
        if streamer.get("chzzk_id"):
            is_live, _, _, _ = await check_chzzk_status(streamer["chzzk_id"])
            if is_live:
                streamer["is_live"] = True
                print(f" - [방송 중 감지됨] {streamer['name']} (알림 스킵)")
            else:
                streamer["is_live"] = False
    print("✨ 방송 상태 동기화 완료!")

    if not live_and_chat_monitor.is_running():
        live_and_chat_monitor.start()


if __name__ == "__main__":
    keep_alive()
    bot.run(TOKEN)