import aiohttp
import pysmartthings
import asyncio
import requests


async def run(api_key, device_id, set_power):
    async with aiohttp.ClientSession() as session:
        api = pysmartthings.SmartThings(session, api_key)
        device = (await api.devices(device_ids=[device_id]))[0]
        await device.status.refresh()
        if set_power:
            await device.switch_on()
        else:
            await device.switch_off()

async def waiter(api_key, device_id, set_power):
    await run(api_key, device_id, set_power)
