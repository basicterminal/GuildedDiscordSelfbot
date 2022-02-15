import discord, json
from discord.ext import commands

import time, os, random, requests
import threading

class multitask:
      bot = commands.Bot(
            self_bot = True,
            command_prefix = "mt!"
      )

      bot.remove_command('help')
      
      class text:
            class codeblocks:
                  spacing = '     '
                  
      class guilded:
            class author:
                   user_name  = ''
                   user_id    = ''
                   user_email = ''
                   user_pass  = ''
                   data       = ''
            
            def login(
                user_email: str = '', 
                user_password: str = ''
            ): 
                r = requests.post(
                    "https://www.guilded.gg/api/login",
                    json = {
                            'getMe'    : True, 
                            'email'    : user_email, 
                            'password' : user_password
                    }
                )

                if r.status_code in [200, 201, 203, 204]:
                   multitask.guilded.author.user_name = r.json()['user']['name']
                   multitask.guilded.author.user_id   = r.json()['user']['id']
                   multitask.guilded.author.user_mail = r.json()['user']['email']
                   multitask.guilded.author.user_pass = user_password

                   multitask.guilded.author.session   = r.cookies['hmac_signed_session']
                

@multitask.bot.event
async def on_ready():   
      with open('multitask/config.json', 'r') as _multi:
           multi = json.load(_multi)
           multitask.guilded.login(
                     user_email = multi['guilded']['email'],
                     user_password = multi['guilded']['password']
           ) 

           if multitask.guilded.author.user_name != '':
              print('[!] Guilded Loaded')
              print("--------------------------")


      ## Multitask
      print('[!] Client: %s' % (multitask.bot.user.name))
      print('[!] Guilded: %s' % (multitask.guilded.author.user_name))
      print("--------------------------")

      for command in multitask.bot.commands:
          print('[*] %s Loaded' % (command.name))


@multitask.bot.command()
async def help(ctx):
      await ctx.send(
            '''```\n<Multitask>\n# Guilded%s|%s# Discord\n- send%s%s%s-help```''' % (multitask.text.codeblocks.spacing, multitask.text.codeblocks.spacing, multitask.text.codeblocks.spacing, multitask.text.codeblocks.spacing, multitask.text.codeblocks.spacing)
      )

@multitask.bot.command(aliases=['bot'])
async def send(ctx, invite, amount: int = 5):
      try:
         with open('multitask/input/hmac.txt', 'r') as _hmac: 
              if int(len(_hmac.readlines())) == 0:
                 await ctx.send('```\nMultitask : HMACs Empty```')
              else:
                 hmacs =  []
                 hmacs += [hmac.strip() for hmac in _hmac.readlines()]
              
              for i in range(int(amount)):
                  requests.put(
                           'https://guilded.gg/api/invites/%s' % (invite),
                           headers = {
                                   'cookie': "hmac_signed_session=%s" % (random.choice(hmacs))
                           }
                  )
      except:
         await ctx.send('```\nMultitask: Error```' )
      

with open('multitask/config.json', 'r') as _multi:
     multi = json.load(_multi)
     multitask.bot.run(multi["discord"]['token'], bot = False)
