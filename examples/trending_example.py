from TikTokApi import TikTokApi
import asyncio
import os
import json

ms_token = os.environ.get("ms_token", None) 


async def trending_videos():
    async with TikTokApi() as api:
        await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=3)
        video_list = []  # List to store video dictionaries

        async for video in api.trending.videos(count=1):

            #video stats
            print(video.id)
            print(video.url)
            print(video.create_time)
            print(video.stats['collectCount'])
            print(video.stats['commentCount'])
            print(video.stats['diggCount'])
            print(video.stats['playCount'])
            print(video.stats['shareCount'])
     

            #author details
            print(video.author.user_id) 
            print(video.author.username)
           

            #sound details
            print(video.sound.id)
            print(video.sound.title)
            print(video.sound.duration)
            print(video.sound.original)

            #all hashtags of a video
            for i in video.hashtags:
                print(i.name)

            video_list.append(video.as_dict)

        # Write the list of video dictionaries as a JSON array to the file
        with open("jsonresponse.json", 'w', encoding='utf-8') as f:
            json.dump(video_list[0], f, ensure_ascii=False)




if __name__ == "__main__":
    asyncio.run(trending_videos())
