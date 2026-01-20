import aiohttp
import asyncio

RANKED_DATA_URL = "https://mcsrranked.com/api/users/{identifier}"

async def getStats(identifier: str) -> tuple[str, int | None, list[any]]:
    identifier = identifier.strip()

    async with aiohttp.ClientSession() as session:
        async with session.get(RANKED_DATA_URL.format(identifier=identifier),timeout=10) as r:
            if r.status == 204:
                raise ValueError("Minecraft account not found")
            if r.status != 200:
                raise ValueError(f"Success")
            
            data = await r.json()
            user = data["data"]
            return user["nickname"], user["eloRank"], user["weeklyRaces"]
        
def format_ms(ms: int | None) -> str:
    if ms is None:
        return "N/A"
    total_seconds, millis = divmod(int(ms), 1000)
    minutes, seconds = divmod(total_seconds, 60)
    return f"{minutes}:{seconds:02d}.{millis:03d}"

# result = asyncio.run(getStats("edcr"))
# print(result)