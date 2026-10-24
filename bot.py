import os
import discord
from discord.ext import tasks, commands
import datetime
import pytz

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

# 🌟 스텔라이브 멤버 기념일 데이터 (연, 월, 일)
ANNIVERSARIES = {
    "강지": {"birthday": (1997, 5, 14), "debut": (2018, 1, 1)},
    "유니": {"birthday": (2003, 5, 21), "debut": (2023, 1, 8)},
    "후야": {"birthday": (2005, 7, 7), "debut": (2025, 9, 20)},
    "히나": {"birthday": (2003, 1, 5), "debut": (2023, 6, 10)},
    "시로": {"birthday": (2003, 2, 22), "debut": (2023, 6, 10)},
    "리제": {"birthday": (2003, 10, 1), "debut": (2023, 6, 11)},
    "타비": {"birthday": (2003, 9, 7), "debut": (2023, 6, 11)},
    "부키": {"birthday": (2004, 3, 21), "debut": (2024, 5, 18)},
    "린": {"birthday": (2004, 5, 3), "debut": (2024, 5, 18)},
    "나나": {"birthday": (2004, 8, 7), "debut": (2024, 5, 19)},
    "리코": {"birthday": (2004, 4, 13), "debut": (2024, 5, 19)},
    "토아": {"birthday": (2006, 11, 22), "debut": (2026, 10, 17)},
    "랑": {"birthday": (2006, 8, 22), "debut": (2026, 10, 17)},
    "요리": {"birthday": (2006, 3, 31), "debut": (2026, 10, 18)},
    "메리": {"birthday": (2006, 6, 13), "debut": (2026, 10, 18)},
    "스텔라이브(공식)": {"birthday": (2022, 6, 25), "debut": (2022, 12, 19)}
}

# 알림 보낼 디스코드 채널 ID (숫자만)
TARGET_CHANNEL_ID = 1562773780823281714

@bot.event
async def on_ready():
    print(f'✅ {bot.user.name} 기념일 알림 봇 준비 완료!')
    if not check_anniversary.is_running():
        check_anniversary.start()

@tasks.loop(hours=1)
async def check_anniversary():
    kst = pytz.timezone('Asia/Seoul')
    now = datetime.datetime.now(kst)
    
    # 매일 아침 9시 정각 체크
    if now.hour == 9:
        channel = bot.get_channel(TARGET_CHANNEL_ID)
        if not channel:
            print("❌ 채널을 찾을 수 없어.")
            return

        today_m, today_d = now.month, now.day

        for name, dates in ANNIVERSARIES.items():
            b_year, b_month, b_day = dates["birthday"]
            d_year, d_month, d_day = dates["debut"]

            # 생일 알림
            if (b_month, b_day) == (today_m, today_d):
                age_anniv = now.year - b_year
                await channel.send(f"🎉 **{name}**의 생일을 축하합니다! 🎂")

            # 데뷔주년 알림 (데뷔 당해년도는 제외)
            if (d_month, d_day) == (today_m, today_d):
                years_passed = now.year - d_year
                if years_passed > 0:
                    await channel.send(f"🌟 **{name}**의 데뷔 **{years_passed}주년**입니다! 모두 축하해 주세요! 🎤")

# Render의 Environment Variable(DISCORD_TOKEN)에서 토큰 가져오기
TOKEN = os.getenv('DISCORD_TOKEN')
if TOKEN:
    bot.run(TOKEN)
else:
    print("❌ DISCORD_TOKEN 환경 변수가 설정되지 않았어!")