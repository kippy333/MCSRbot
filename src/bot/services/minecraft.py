import aiohttp

MOJANG_PROFILE_URL = "https://api.mojang.com/users/profiles/minecraft/{username}"

async def UsernameToUuid(username: str) -> tuple[str, str]:
    username = username.strip()

    async with aiohttp.ClientSession() as session:
        async with session.get(MOJANG_PROFILE_URL.format(username=username),timeout=10) as r:
            if r.status == 204:
                raise ValueError("Minecraft account not found")
            if r.status != 200:
                raise ValueError(f"Mojang API error (HTTP {r.status})")
            
            data = await r.json()
            return data["id"], data["name"]