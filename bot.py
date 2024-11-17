from telethon import TelegramClient, events
from telethon.tl.types import DocumentAttributeVideo
from moviepy.editor import VideoFileClip
from ethon.telefunc import fast_upload
from ethon.pyfunc import video_metadata
import requests
import os, time
import math
#import subprocess
from PIL import Image


# Replace these with your own values
API_ID = os.getenv('apiid')
API_HASH = os.getenv('apihash')
BOT_TOKEN = os.getenv('tk')

# Create the bot client
bot = TelegramClient('bot_session', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# Function to format the progress percentage
def progress_bar(completed, total, length=20):
    progress = int(length * completed / total)
    return '[' + '=' * progress + ' ' * (length - progress) + ']'

# Function to generate a thumbnail from the video
#def generate_thumbnail(video_path, thumbnail_path='thumb.jpg'):
    #command = f'ffmpeg -i "{video_path}" -ss 00:00:01.000 -vframes 1 "{thumbnail_path}" -y'
    #subprocess.run(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    #return thumbnail_path if os.path.exists(thumbnail_path) else None

@bot.on(events.NewMessage(pattern='/upload'))
async def upload_from_url(event):
    try:
        # Extract the URL from the message
        if len(event.message.message.split()) < 2:
            await event.reply("Please provide a URL!")
            return

        url = event.message.message.split()[1]
        reply_msg = await event.reply("Starting download...")

        # Start downloading the file
        response = requests.get(url, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        filename = url.split("/")[-1]  # Extract the filename from the URL
        
        downloaded_size = 0
        with open(filename, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
                    downloaded_size += len(chunk)
                    # Update progress every 2%
                    if total_size > 0 and downloaded_size % (total_size // 50) == 0:
                        progress = progress_bar(downloaded_size, total_size)
                        percent = (downloaded_size / total_size) * 100
                        await reply_msg.edit(f"Downloading: {progress} {percent:.2f}%")

        await reply_msg.edit("Download complete. Generating thumbnail...")

        # Generate thumbnail
        #thumbnail_path = generate_thumbnail(filename)
        
        await reply_msg.edit("Thumbnail generated. Uploading to Telegram...")

        # Upload the file to Telegram using fast_upload
        #uploaded_file = await fast_upload(bot, filename)

        # Send the uploaded file with the thumbnail
        #await bot.send_file(
           #event.chat_id,
           # uploaded_file,
           #  caption=f'Uploaded: {filename}',
           #   thumb=thumbnail_path,
           #  supports_streaming=True  # This makes the video streamable
        #)
        
        # Clean up the local file and thumbnail after uploading
        #os.remove(filename)
        #if thumbnail_path and os.path.exists(thumbnail_path):
            #os.remove(thumbnail_path)

        try:
        #jpg = await gen_thumb(out)
          thumb_path='thumb.jpg'
          with VideoFileClip(file_name) as video:
              frame = video.get_frame(3.0)
              img = Image.fromarray(frame)
              img.save(thumb_path, "JPEG")
          metadata = video_metadata(out)
          width = metadata["width"]
          height = metadata["height"]
          duration = metadata["duration"]
          attributes = [DocumentAttributeVideo(duration=duration, w=width, h=height, supports_streaming=True)]           
          UT = time.time()
          uploader = await fast_upload(f'{file_name}', f'{file_name}', UT, bot, reply_msg, '**UPLOADING:**')
          await bot.send_file(event.chat_id, uploader,thumb=thumb_path, caption="**RvX**", attributes=attributes, force_document=False)
          if os.path.exists(thumb_path):
             os.remove(thumb_path)
        except Exception as e:
          print(e)
          return await reply_msg.edit(f"An error occured while uploading!\n\n{e}")
        #await edit.delete()
        os.remove(file_name)
        await reply_msg.edit("Upload complete!")
    except Exception as e:
        await event.reply(f"An error occurred: {str(e)}")

# Start the bot
print("Bot is running...")
bot.run_until_disconnected()
