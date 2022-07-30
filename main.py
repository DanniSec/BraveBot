from requests import request
import config

# import the necessary modules for discord bot 
import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord.ui import Button, View

import requests
import json
import random

# from the config file import the token and prefix
TOKEN = config.token
PREFIX = config.prefix


# prefix
bot = commands.Bot(command_prefix=PREFIX, intents=discord.Intents.all())


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.command(name="ping", description="Returns the latency of the bot", brief="Returns the latency of the bot", aliases=["pong"])
async def ping(ctx):
    await ctx.send('Pong!')
    latency = bot.latency
    await ctx.send(f"Took {latency:02f} to respond.")


# generate build from ultimate-bravery.net and send it as embed to the channel
@bot.command(name="brave", description="Generates a build from ultimate-bravery.net", brief="Generates a build from ultimate-bravery.net", aliases=["b", "Imbrave", "elorip"])
async def brave(ctx, role="all", champion="all"):
    button = Button(label="I'm blind", style=discord.ButtonStyle.green, emoji="🔍")
    url_button = Button(label="Rules", url="https://ultimate-bravery.net/rules")
    
    view = View()
    view.add_item(button)
    view.add_item(url_button)
    

    build = generate_build(role_list[role], champion_list[champion])
    # print(build)
    
    items_to_build = build['data']['items']
    item_list = [*items_to_build]

    summoners = build['data']['summonerSpells']
    summs = [*summoners]

    runes_list = build['data']['runes']
    runes_types = [runes_list['primary'], runes_list['secondary'], runes_list['stats']]
    runes = [*runes_types] 

    # lists of runes (primary secondary and stats)
    primary_runes = [*(runes[0].keys())]
    secondary_runes = [*(runes[1].keys())]
    stats_runes = []

    # list of stat runes
    for stat in runes[2]:
        description = stat['description']
        stats_runes.append(description)
    
    # button callback
    async def button_callback(interaction):
        await interaction.response.send_message(f"{rune_icons[primary_runes[0]]}\n{rune_icons[primary_runes[1]]}   {rune_icons[secondary_runes[0]]}\n{rune_icons[primary_runes[2]]}   {rune_icons[secondary_runes[1]]} \n{rune_icons[primary_runes[3]]}   {rune_icons[stats_runes[0]]}\n<:air:1002409132638343219>   {rune_icons[stats_runes[1]]}\n<:air:1002409132638343219>   {rune_icons[stats_runes[2]]}")
    
    button.callback = button_callback

    # Embed
    embed = discord.Embed(title=f"{build['data']['title']} {build['data']['champion']['name']}", description=build['data']['role'], color=0x00ff00)

    # check what type of smite is used
    if build['data']['roleSpecificItem'] != None:
        
        if build['data']['role'] == "Jungle":
            jg_items = ["Emberknife (Red smite)", "Hailblade (Blue smite)"]
            # pick one item in jg_items at random
            roleSpecificItem = random.choice(jg_items)
            embed.add_field(name="Jungle item", value=roleSpecificItem, inline=True)

        if build['data']['role'] == "Support":
            supp_items = ["Spectral Sickle", "Steel Shoulderguards", "Spellthief's Edge", "Relic Shield"]
            roleSpecificItem = random.choice(supp_items)
            embed.add_field(name="Support item", value=roleSpecificItem, inline=True)
        
    else:
        roleSpecificItem = None
    

    # create embed  
    
    embed.set_author(name="ULTIMATE BRAVERY", url=f"https://ultimate-bravery.net/Classic?s={build['data']['seedId']}", icon_url=build['data']['champion']['image'])
    embed.set_thumbnail(url=build['data']['roleSpecificItem'] if build['data']['roleSpecificItem'] != None else build['data']['champion']['image'])
    embed.set_footer(text=build['data']['seedId'], icon_url=ctx.message.author.avatar.url)
    embed.add_field(name="Build", value=f"\n{item_list[0]}\n{item_list[1]}\n{item_list[2]}\n{item_list[3]}\n{item_list[4]}\n{item_list[5]}\n*Cost: {build['data']['totalCost']}*\n", inline=True)
    embed.add_field(name="Ability to max", value=build['data']['champion']['spell']['key'], inline=True)
    embed.add_field(name="Summoner Spells", value=f"{summs[0]} + {summs[1]}", inline=True)
    
    embed.add_field(name="Runes", value=f"{rune_icons[primary_runes[0]]}\n{rune_icons[primary_runes[1]]}   {rune_icons[secondary_runes[0]]}\n{rune_icons[primary_runes[2]]}   {rune_icons[secondary_runes[1]]} \n{rune_icons[primary_runes[3]]}", inline=True)
    embed.add_field(name="Stats", value=f"{rune_icons[stats_runes[0]]}\n{rune_icons[stats_runes[1]]}\n{rune_icons[stats_runes[2]]}", inline=True)
    # send embed
    await ctx.send(embed=embed, view=view)



def generate_build(roles, champions):
    url = "https://api2.ultimate-bravery.net/bo/api/ultimate-bravery/v1/classic/dataset/"

    payload = "{\"map\":11,\"level\":10,\"roles\":[" + roles + "],\"language\":\"en\",\"champions\":[" + champions +"]}"
    headers = {
    'Content-Type': 'application/json;charset=UTF-8'
    }

    data = requests.post(url, headers=headers, data=payload)
    
    return data.json()


role_list = {
    "top": "0",
    "mid": "1",
    "jg": "2",
    "bot": "3",
    "supp": "4",
    "all": "0,1,2,3,4"
}

champion_list = {
    "Aatrox": "266",
    "Ahri": "103",
    "Akali": "84",
    "Akshan": "166",
    "Alistar": "12",
    "Amumu": "32",
    "Anivia": "34",
    "Annie": "1",
    "Aphelios":"523",
    "Ashe": "22",
    "Aurelion Sol": "136",
    "Azir": "268",
    "Bard": "432",
    "Bel'Veth": "200",
    "Blitzcrank": "53",
    "Brand": "63",
    "Braum": "201",
    "Caitlyn": "51",
    "Camille": "164",
    "Cassiopeia": "69",
    "Cho'Gath": "31",
    "Corki": "42",
    "Darius": "122",
    "Diana": "131",
    "Draven": "119",
    "Dr. Mundo": "36",
    "Ekko": "245",
    "Elise": "60",
    "Evelynn": "28",
    "Ezreal": "81",
    "Fiddlesticks": "9",
    "Fiora": "114",
    "Fizz": "105",
    "Galio": "3",
    "Gangplank": "41",
    "Garen": "86",
    "Gnar": "150",
    "Gragas": "79",
    "Graves": "104",
    "Gwen": "887",
    "Hecarim": "120",
    "Heimerdinger": "74",
    "Illaoi": "420",
    "Irelia": "39",
    "Ivern": "427",
    "Janna": "40",
    "Jarvan IV": "59",
    "Jax": "24",
    "Jayce": "126",
    "Jhin": "202",
    "Jinx": "222",
    "Kai'Sa": "145",
    "Kalista": "429",
    "Karma": "43",
    "Karthus": "30",
    "Kassadin": "38",
    "Katarina": "55",
    "Kayle": "10",
    "Kayn": "141",
    "Kennen": "85",
    "Kha'Zix": "121",
    "Kindred": "203",
    "Kled": "240",
    "Kog'Maw": "96",
    "LeBlanc": "7",
    "Lee Sin": "64",
    "Leona": "89",
    "Lillia": "876",
    "Lissandra": "127",
    "Lucian": "236",
    "Lulu": "117",
    "Lux": "99",
    "Malphite": "54",
    "Malzahar": "90",
    "Maokai": "57",
    "Master Yi": "11",
    "Miss Fortune": "21",
    "Wukong": "62",
    "Mordekaiser": "82",
    "Morgana": "25",
    "Nami": "267",
    "Nasus": "75",
    "Nautilus": "111",
    "Neeko": "518",
    "Nidalee": "76",
    "Nocturne": "56",
    "Nunu & Willump": "20",
    "Olaf": "2",
    "Orianna": "61",
    "Ornn": "516",
    "Pantheon": "80",
    "Poppy": "78",
    "Pyke": "555",
    "Qiyana": "246",
    "Quinn": "133",
    "Rakan": "497",
    "Rammus": "33",
    "Rek'Sai": "421",
    "Renata Glasc": "888",
    "Renekton": "58",
    "Riven": "92",
    "Rumble": "68",
    "Ryze": "13",
    "Samira": "360",
    "Sejuani": "113",
    "Senna": "235",
    "Seraphine": "147",
    "Sett": "875",
    "Shaco": "35",
    "Shen": "98",
    "Shyvana": "102",
    "Singed": "27",
    "Sion": "14",
    "Sivir": "15",
    "Skarner": "72",
    "Sona": "37",
    "Soraka": "16",
    "Swain": "50",
    "Sylas": "517",
    "Syndra": "134",
    "Tahm Kench": "223",
    "Taliyah": "163",
    "Talon": "91",
    "Taric": "44",
    "Teemo": "17",
    "Thresh": "412",
    "Tristana": "18",
    "Trundle": "48",
    "Tryndamere": "23",
    "Twisted Fate": "4",
    "Twitch": "29",
    "Udyr": "77",
    "Urgot": "6",
    "Varus": "110",
    "Vayne": "67",
    "Veigar": "45",
    "Vel'Koz": "161",
    "Vex": "711",
    "Vi": "254",
    "Viego": "234",
    "Viktor": "112",
    "Vladimir": "8",
    "Volibear": "106",
    "Warwick": "19",
    "Xayah": "498",
    "Xerath": "101",
    "Xin Zhao": "157",
    "Yasuo": "157",
    "Yone": "777",
    "Yorick": "83",
    "Yuumi": "350",
    "Zac": "154",
    "Zed": "238",
    "Zeri": "221",
    "Ziggs": "115",
    "Zilean": "26",
    "Zoe": "142",
    "Zyra": "143",
    "all": "266,103,84,166,12,32,34,1,523,22,136,268,432,53,63,201,51,164,69,31,42,122,131,119,36,245,60,28,81,9,114,105,3,41,86,150,79,104,887,120,74,420,39,427,40,59,24,126,202,222,145,429,43,30,38,55,10,141,85,121,203,240,96,7,64,89,876,127,236,117,99,54,90,57,11,21,62,82,25,267,75,111,518,76,56,20,2,61,516,80,78,555,246,133,497,33,421,526,58,107,92,68,13,360,113,235,147,875,35,98,102,27,14,15,72,37,16,50,517,134,223,163,91,44,17,412,18,48,23,4,29,77,6,110,67,45,161,711,254,234,112,8,106,19,498,101,5,157,777,83,350,154,238,221,115,26,142,143"
}
# Rune list
rune_icons = {
    "Arcane Comet": "<:Rune_Arcane_Comet:1001780695322083459>", # srocery
    "Phase Rush": "<:Rune_Phase_Rush:1001780990202630196>", # sorcery
    "Absolute Focus": "<:Rune_Absolute_Focus:1001780690985156718>", # sorcery
    "Adaptive Force (6 AD or 10 AP)": "<:Rune_Adaptive_Force:1001780692042137600>", # stats
    "Aftershock": "<:Rune_Aftershock:1001780693325598790>", # resolve
    "Approach Velocity": "<:Rune_Approach_Velocity:1001780694537752596>", # inspiration
    "Armor (5 Armor)": "<:Rune_Armor:1001780696848810024>", # stats
    f"Attack Speed (9% Attack Speed)": "<:Rune_Attack_Speed:1001780697587011585>", # stats
    "Biscuit Delivery": "<:Rune_Biscuit_Delivery:1001780689588465734>", # inspiration
    "Bone Plating": "<:Rune_Bone_Plating:1001780817489563708>", # resolve
    "Celerity": "<:Rune_Celerity:1001780818710110269>", # sorcery
    "Cheap Shot": "<:Rune_Cheap_Shot:1001780819922268180>", # domination
    "Conditioning": "<:Rune_Conditioning:1001780821033766993>", # resolve
    "Conqueror": "<:Rune_Conqueror:1001780822375931904>", # precision
    "Scaling Cooldown Reduction (1-10% CDR, lvls 1-18)": "<:Rune_Cooldown_Reduction:1001780823600676995>", # stats
    "Cosmic Insight": "<:Rune_Cosmic_Insight:1001780824728948797>", # inspiration
    "Coup de Grace": "<:Rune_Coup_de_Grace:1001780816147382352>", # precision
    "Cut Down": "<:Rune_Cut_Down:1001780849110433843>", # precision
    "Dark Harvest": "<:Rune_Dark_Harvest:1001780850200944701>", # domination
    "Demolish": "<:Rune_Demolish:1001780851526357012>", # resolve
    "Electrocute": "<:Rune_Electrocute:1001780853115977808>", # domination
    "Eyeball Collection": "<:Rune_Eyeball_Collection:1001780854298771576>", # domination
    "Fleet Footwork": "<:Rune_Fleet_Footwork:1001780855489966100>", # precision
    "Font of Life": "<:Rune_Font_of_Life:1001780858870567024>", # resolve
    "Future's Market": "<:Rune_Futures_Market:1001780860531515534>", # inspiration
    "Gathering Storm": "<:Rune_Gathering_Storm:1001780862003728505>", # sorcery
    "Ghost Poro": "<:Rune_Ghost_Poro:1001780863387840523>", # domination
    "Glacial Augment": "<:Rune_Glacial_Augment:1001780864830672967>", # inspiration
    "Grasp of the Undying": "<:Rune_Grasp_of_the_Undying:1001780865887653888>", # resolve
    "Guardian": "<:Rune_Guardian:1001780867204657164>", # resolve
    "Hail of Blades": "<:Rune_Hail_of_Blades:1001780868391653468>", # domination
    "Scaling Health (15-90 HP, lvls 1-18)": "<:Rune_Health:1001780869675089920>", # stats
    "Hextech Flashtraption": "<:Rune_Hextech_Flashtraption:1001780847743090800>", # inspiration
    "Ingenious Hunter": "<:Rune_Ingenious_Hunter:1001780902822682704>", # domination
    "Last Stand": "<:Rune_Last_Stand:1001780904022253659>", # precision
    "Legend: Alacrity": "<:Rune_Legend__Alacrity:1001780905775480832>", # precision
    "Legend: Bloodline": "<:Rune_Legend__Bloodline:1001780907163791380>", # precision
    "Legend: Tenacity": "<:Rune_Legend__Tenacity:1001780910670221343>", # precision
    "Lethal Tempo": "<:Rune_Lethal_Tempo:1001780912066920569>", # precision
    "Magic Resist (6 MR)": "<:Rune_Magic_Resistance:1001780913258111047>", # stats
    "Magical Footwear": "<:Rune_Magical_Footwear:1001780901677649971>", # inspiration
    "Manaflow Band": "<:Rune_Manaflow_Band:1001780977695199252>", # sorcery
    "Minion Dematerializer": "<:Rune_Minion_Dematerializer:1001780980488618057>", # inspiration
    "Nimbus Cloak": "<:Rune_Nimbus_Cloak:1001780981440712815>", # sorcery
    "Overgrowth": "<:Rune_Overgrowth:1001780985140088976>", # resolve
    "Overheal": "<:Rune_Overheal:1001780987040112752>", # precision
    "Perfect Timing": "<:Rune_Perfect_Timing:1001780988889792602>", # inspiration
    "Predator": "<:Rune_Predator:1001780976415952997>", # domination
    "Presence of Mind": "<:Rune_Presence_of_Mind:1001781715439726673>", # precision
    "Press the Attack": "<:Rune_Press_the_Attack:1001781713980104784>", # precision
    "First Strike": "<:Rune_First_Strike:1001789028640768070>", # inspiration
    "Relentless Hunter": "<:Rune_Relentless_Hunter:1001789029718700152>", # domination
    "Revitalize": "<:Rune_Revitalize:1001789030792433735>", # resolve
    "Scorch": "<:Rune_Scorch:1001789031929106502>", # sorcery
    "Second Wind": "<:Rune_Second_Wind:1001789032935719003>", # resolve
    "Shield Bash": "<:Rune_Shield_Bash:1001789034420506674>", # resolve
    "Sudden Impact": "<:Rune_Sudden_Impact:1001789035674607686>", # domination
    "Summon Aery": "<:Rune_Summon_Aery:1001789037050343515>", # sorcery
    "Taste of Blood": "<:Rune_Taste_of_Blood:1001789038304436304>", # domination
    "Transcendence": "<:Rune_Transcendence:1001789017492291657>", # sorcery
    "Treasure Hunter": "<:Rune_Treasure_Hunter:1001789018930946098>", # domination
    "Triumph": "<:Rune_Triumph:1001789020214403092>", # precision
    "Ultimate Hunter": "<:Rune_Ultimate_Hunter:1001789021401395260>", # domination
    "Unflinching": "<:Rune_Unflinching:1001789023053938708>", # resolve
    "Unsealed Spellbook": "<:Rune_Unsealed_Spellbook:1001789024287064104>", # inspiration
    "Waterwalking": "<:Rune_Waterwalking:1001789025402765332>", # inspiration
    "Zombie Ward": "<:Rune_Zombie_Ward:1001789026707197972>", # domination
    "Time Warp Tonic": "<:Rune_Time_Warp_Tonic:1002035120930299915>", # inspiration
    "Nullifying Orb": "<:Rune_Nullifying_Orb:1002035881932238899>", # sorcery
}


# run bot
bot.run(TOKEN)