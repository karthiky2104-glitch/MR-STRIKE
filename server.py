import asyncio

def worker():
    print("Server thread running...")

async def main():
    response = await asyncio.to_thread(worker)
    print(response)

if __name__ == "__main__":
    asyncio.run(main())