import asyncio
import datetime
import time

from twitchbot import Message, Command, Mod, add_task, stop_task, channels

pings = -1


@Command('ping', cooldown=3)
async def cmd_ping(msg: Message, *args):
    global pings
    pings += 1
    await msg.reply(f'Pong #{pings}')

# class MidnightMod(Mod):
#     name = 'midnight'
#     last_message_diff = datetime.datetime.min
#
#     async def loaded(self):
#         add_task('midnight_message', self.midnight_check())
#
#     async def unloaded(self):
#         stop_task('midnight_message')
#
#     async def midnight_check(self):
#         while True:
#             utc_now = datetime.datetime.utcnow()
#             if utc_now.hour == 0 and abs((self.last_message_diff - utc_now).total_seconds()) > (60 * 61):
#                 await channels['CHANNEL_NAME'].send_message('MESSAGE HERE')
#                 self.last_message_diff = datetime.datetime.utcnow()
#             await asyncio.sleep(10)

# @Command('whisper', context=CommandContext.WHISPER)
# async def cmd_whisper(msg: Message, *args):
#     await msg.reply('got it!')

# @Command('shoutout', permission='shoutout')
# async def cmd_shoutout(msg: Message, *args):
#     info = await get_user_info(args[0])
#     date = format_datetime(await get_user_creation_date(args[0]))
#     followers = await get_user_followers(args[0])
#
#     await msg.reply(f'go give {args[0]} a follow at {f"https://twitch.tv/{args[0]}"}')
#     await msg.reply(
#         f'{args[0]} with {followers.follower_count} followers and {info.view_count} views * created at {date}')

# @Command('test')
# async def cmd_test(msg: Message, *args):
#     await msg.reply(f'{format_datetime(await get_user_creation_date(msg.author))}')
