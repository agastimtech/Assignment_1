#importing libraries
import asyncio
import random
import aiofiles

async def create_pseudo_string():
    # Create pseudo string with 50% probablity of 'Maruti' keyword
    if random.random()<0.5:
        return 'Other String'
    else:
        return 'MARUTI'
async def write_to_file(file_path):
    # write the pseudo string in files
    while True:
        pseudo_string = await create_pseudo_string()
        async with aiofiles.open(file_path,'a') as f:
            await f.write(pseudo_string+'\n')
        await asyncio.sleep(1)
async def count_occurences(file_path):
    #count occurences of 'MARUTI' keyword
    count=0
    async with aiofiles.open(file_path,'r') as f:
        async for line in f:
            if 'MARUTI' in line:
                count+=1
    return count
async def monitor_files(file1_path,file2_path,counts_log_path):
    while True:
        file1_count = await count_occurences(file1_path)
        file2_count = await count_occurences(file2_path)
        counts_log = f'File1_count: {file1_count}, File2_count: {file2_count}\n'
        # write counts to the log file
        async with aiofiles.open(counts_log_path,'w') as f:
            await f.write(counts_log)
        await asyncio.sleep(1)

file1_path='file1.txt'
file2_path='file2.txt'
counts_log_path='counts.log'

async def main():
        tasks=[asyncio.create_task(write_to_file(file1_path)),
               asyncio.create_task(write_to_file(file2_path)),
               asyncio.create_task(monitor_files(file1_path,file2_path,counts_log_path))]
        await asyncio.gather(*tasks)

        loop=asyncio.get_event_loop()
        try:
            loop.run_until_complete(asyncio.gather(*tasks))
        finally:
            loop.close()
if __name__=="__main__":
    asyncio.run(main())
