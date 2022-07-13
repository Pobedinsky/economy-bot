import discord
from discord.ext import commands
import json
import os
import random

client = commands.Bot(command_prefix = ",")

@client.event
async def on_command_error(ctx, error):
  if isinstance(error, commands.CommandOnCooldown):
    
    msg = discord.Embed(title = " ", color = discord.Color.red())
    msg.add_field(name = "Cooldown!", value = "You can do this command again in {:.2f}s".format(error.retry_after))
  
    await ctx.send(embed = msg)



@client.event
async def on_ready():
  print("Ready")

@client.command()
async def balance(ctx):
  await open_account(ctx.author)
  user = ctx.author
  users = await get_bank_data()
  wallet_amt = users[str(user.id)]["cash"]
  bank_amt = users[str(user.id)]["bank"]

  
  em = discord.Embed(title = " ", color = discord.Color.green())
  em.set_author(name=f"{ctx.author}", icon_url=ctx.author.avatar_url)
  em.add_field(name = "Cash:", value = f"€ {wallet_amt}")
  em.add_field(name = "Bank:", value = f"€ {bank_amt}")
  em.add_field(name = "Total:", value = f"€ {bank_amt+wallet_amt}")
  await ctx.send(embed = em)


@client.command()
async def bal(ctx):
  await open_account(ctx.author)
  user = ctx.author
  users = await get_bank_data()
  wallet_amt = users[str(user.id)]["cash"]
  bank_amt = users[str(user.id)]["bank"]

  
  em = discord.Embed(title = " ", color = discord.Color.green())
  em.set_author(name=f"{ctx.author}", icon_url=ctx.author.avatar_url)
  em.add_field(name = "Cash:", value = f"€ {wallet_amt}")
  em.add_field(name = "Bank:", value = f"€ {bank_amt}")
  em.add_field(name = "Total:", value = f"€ {bank_amt+wallet_amt}")
  await ctx.send(embed = em)
  


@client.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def beg(ctx):
  await open_account(ctx.author)
  user = ctx.author
  users = await get_bank_data()

  earnings = random.randrange(101)
  em = discord.Embed(title = " ", color = discord.Color.green())
  em.set_author(name=f"{ctx.author}", icon_url=ctx.author.avatar_url)
  em.add_field(name = "Oh, poor guy!", value = f"Someone gave you {earnings} euros!")
  
  await ctx.send(embed = em)


  users[str(user.id)]["cash"]+= earnings

  with open("mainbank.json","w") as f:
    json.dump(users,f)




@client.command()
async def withdraw(ctx, amount = None):
  await open_account(ctx.author)
  
  if amount == None:
    await ctx.send ("Plese enter the amount")
    return

  bal = await update_bank(ctx.author)

  if amount == "all":
    await update_bank(ctx.author, bal[1])
    await update_bank(ctx.author, -1*bal[1], "bank")
    em = discord.Embed(title = " ", description = f"You withdrew € {bal[1]}!", color = discord.Color.green())
    em.set_author(name=f"{ctx.author}", icon_url=ctx.author.avatar_url)
  
    await ctx.send(embed = em)


  if amount != "all":  
    amount = int(amount)
  
    if amount > bal[1]:
      await ctx.send ("You don't have that much money!")
      return  

    if amount<0:
      await ctx.send("Amount must be positive!")
      return


    await update_bank(ctx.author, amount)
    await update_bank(ctx.author, -1*amount, "bank")
    em = discord.Embed(title = " ", description = f"You withdrew € {bal[1]}!", color = discord.Color.green())
    em.set_author(name=f"{ctx.author}", icon_url=ctx.author.avatar_url)

  
    await ctx.send(embed = em)


#withdraw command but different way



@client.command()
async def w(ctx, amount = None):
  await open_account(ctx.author)
  
  if amount == None:
    await ctx.send ("Plese enter the amount")
    return

  bal = await update_bank(ctx.author)

  if amount == "all":
    await update_bank(ctx.author, bal[1])
    await update_bank(ctx.author, -1*bal[1], "bank")
    em = discord.Embed(title = " ", description = f"You withdrew € {bal[1]}!", color = discord.Color.green())
    em.set_author(name=f"{ctx.author}", icon_url=ctx.author.avatar_url)
  
    await ctx.send(embed = em)


  if amount != "all":  
    amount = int(amount)
  
    if amount > bal[1]:
      await ctx.send ("You don't have that much money!")
      return  

    if amount<0:
      await ctx.send("Amount must be positive!")
      return


    await update_bank(ctx.author, amount)
    await update_bank(ctx.author, -1*amount, "bank")
    em = discord.Embed(title = " ", description = f"You withdrew € {bal[1]}!", color = discord.Color.green())
    em.set_author(name=f"{ctx.author}", icon_url=ctx.author.avatar_url)

  
    await ctx.send(embed = em)






@client.command()
async def deposit(ctx, amount = None):
  await open_account(ctx.author)
  
  if amount == None:
    await ctx.send ("Plese enter the amount")
    return

  bal = await update_bank(ctx.author)

  if amount == "all":
   await update_bank(ctx.author, -1*bal[0])
   await update_bank(ctx.author, bal[0], "bank")
   em = discord.Embed(title = " ", description = f"You deposited {bal[0]} euros!", color = discord.Color.green())
   em.set_author(name=f"{ctx.author}", icon_url=ctx.author.avatar_url)
  
   await ctx.send(embed = em)  

  if amount != "all":
   amount = int(amount)
  
   if amount > bal[0]:
     await ctx.send ("You don't have that much money!")
     return  

   if amount<0:
     await ctx.send("Amount must be positive!")
     return


   await update_bank(ctx.author, -1*amount)
   await update_bank(ctx.author, amount, "bank")
   em = discord.Embed(title = " ", description = f"You deposited {amount} euros!", color = discord.Color.green())
   em.set_author(name=f"{ctx.author}", icon_url=ctx.author.avatar_url)
   await ctx.send(embed = em)

#deposit command but different
    


@client.command()
async def dep(ctx, amount = None):
  await open_account(ctx.author)
  
  if amount == None:
    await ctx.send ("Plese enter the amount")
    return

  bal = await update_bank(ctx.author)

  if amount == "all":
   await update_bank(ctx.author, -1*bal[0])
   await update_bank(ctx.author, bal[0], "bank")
   em = discord.Embed(title = " ", description = f"You deposited {bal[0]} euros!", color = discord.Color.green())
   em.set_author(name=f"{ctx.author}", icon_url=ctx.author.avatar_url)
  
   await ctx.send(embed = em)  

  if amount != "all":
   amount = int(amount)
  
   if amount > bal[0]:
     await ctx.send ("You don't have that much money!")
     return  

   if amount<0:
     await ctx.send("Amount must be positive!")
     return


   await update_bank(ctx.author, -1*amount)
   await update_bank(ctx.author, amount, "bank")
   em = discord.Embed(title = " ", description = f"You deposited {amount} euros!", color = discord.Color.green())
   em.set_author(name=f"{ctx.author}", icon_url=ctx.author.avatar_url)
   await ctx.send(embed = em)

  



@client.command()
async def send(ctx,member:discord.Member, amount = None):
  await open_account(ctx.author)
  await open_account(member)
  
  if amount == None:
    await ctx.send ("Plese enter the amount")
    return

  bal = await update_bank(ctx.author)

  amount = int(amount)
  if amount > bal[1]:
    await ctx.send ("You don't have that much money!")
    return  

  if amount<0:
    await ctx.send("Amount must be positive!")
    return


  await update_bank(ctx.author, -1*amount, "bank")
  await update_bank(member, amount, "bank")

  await ctx.send(f"You gave {amount} euros!")



@client.command()
@commands.cooldown(1, 20, commands.BucketType.user)
async def rob(ctx,member:discord.Member):
  await open_account(ctx.author)
  if (member.id) == 996319238149132389:
    await ctx.send("You can't rob me LMAO")
    return

  if (member.id) == (ctx.author.id):
    await ctx.send("You can't rob yourself, jerk")
    return

  if (member.id) != 996319238149132389:  
    await open_account(member)

    bal = await update_bank(ctx.author)

    if bal[0] < 100:
     await ctx.send ("It's not worth it!")
     return  

    earnings = random.randrange(0, bal[0])  

    await update_bank(ctx.author, earnings)
    await update_bank(member, -1*earnings)

    await ctx.send(f"You robbed {earnings} euros!")
  



@client.command()
async def slots(ctx, amount = None):
  await open_account(ctx.author)
  
  if amount == None:
    await ctx.send ("Plese enter the amount")
    return

  bal = await update_bank(ctx.author)

  amount = int(amount)
  if amount > bal[0]:
    await ctx.send ("You don't have that much money!")
    return  

  if amount<0:
    await ctx.send("Amount must be positive!")
    return
  final = []
  for i in range(3):  
    a = random.choice( ['🍉', '🍋', '🍎'] )
    final.append(a)
    

  if final [0] == final [1] and final [1] == final [2]:
    await update_bank(ctx.author, 2*amount) 
    em = discord.Embed(title = " ", color = discord.Color.green())
    em.set_author(name=f"{ctx.author}", icon_url=ctx.author.avatar_url)
    em.add_field(name = "You won! 😃\n", value = f"{final[0]} {final[1]} {final[2]}")
    await ctx.send(embed = em)
 
  else: 
    await update_bank(ctx.author, -1*amount)
    em = discord.Embed(title = " ", color = discord.Color.red())
    em.set_author(name=f"{ctx.author}", icon_url=ctx.author.avatar_url)
    em.add_field(name = "You lost 😥\n", value = f"{final[0]} {final[1]} {final[2]}")
    await ctx.send(embed = em)






@client.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def work(ctx):
  await open_account(ctx.author)
  user = ctx.author
  users = await get_bank_data()

  earnings = random.randrange(500)


  a = random.choice( [f'You cleaned a toilet and received € {earnings}',
                      f'You stack cups at 7-11 for 8 hours a day, racking up a measly € {earnings}', 
                      f'You work as a janitor and earn € {earnings}',
                      f'You worked in the cafeteria and have earned € {earnings}', 
                      f'You are asked to schedule the animatronics performance times for tomorrow. Your boss pays you € {earnings}',
                     f'One by one, you screw on toothpaste caps for € {earnings}'] )

  em = discord.Embed(title = " ", description = a, color = discord.Color.green())
  em.set_author(name=f"{ctx.author}", icon_url=ctx.author.avatar_url)
  
  await ctx.send(embed = em)


  users[str(user.id)]["cash"]+= earnings

  with open("mainbank.json","w") as f:
    json.dump(users,f)





#auxiliar functions
async def open_account(user):
  users = await get_bank_data()

  if str(user.id) in users:
    return False
  else:
    users[str(user.id)]={}
    users[str(user.id)]["cash"] = 0
    users[str(user.id)]["bank"] = 0

  with open("mainbank.json","w") as f:
    json.dump(users,f)
    return True
    
async def get_bank_data():
  with open("mainbank.json", "r") as f:
    users = json.load(f)
  return users


async def update_bank(user,change = 0,mode = "cash"):
  users = await get_bank_data()
  users[str(user.id)][mode] += change
  
  with open("mainbank.json","w") as f:
    json.dump(users,f)
    bal = [ users[str(user.id)]["cash"],  users[str(user.id)]["bank"]]
    return bal  
  



client.run("TOKEN")
