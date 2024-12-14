import os
import httpx


class DevicesClient:
    def __init__(self):
        self.devices_hostname = os.getenv("DEVICES_MANAGER_HOSTNAME")

    async def get_if_active_groups(self):
        url = f"http://{self.devices_hostname}:8000/device-group/active-groups"
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url)
                response.raise_for_status()
                return response.status_code == 204
        except httpx.HTTPStatusError as e:
            return False
