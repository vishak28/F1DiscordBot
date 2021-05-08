import discord
from discord.ext import commands
import json
import pandas as pd


F1_PREDICTIONS_LOCATION = "./database/f1_predictions.json"
WRONG_COMMAND_MSG = "OOGA BOOGA WRONG COMMAND DUMB BITCH. USE #F1 FOR HELP!" 
DRIVERS = ['HAM',"BOT","VER","PER","LEC","SAI","NOR","RIC","ALO","OCO","GAS","TSU","VET","STR","GIO","RAI","RUS","LAT","MAZ","SCH"]
DRIVERS_COLORS_LOCATION = "./constants/drivers_colors.json"
DRIVERS_JSON_LOCATION = "./constants/drivers.json"

class f1_pred(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def f1(self, ctx):
        with open(DRIVERS_COLORS_LOCATION, 'r') as team_colors_file:
            team_colors = json.load(team_colors_file)
            team_colors_file.close()
        message = '**Commands**\n\n#predict -> to set prediction. Format:\n#predict vet rai maz sch lat\n\n#show -> To show predictions.\n\n#reset -> To reset database.\n\n'
        message += '**Driver names accepted**\n\n'
        count = 1
        for driver in DRIVERS:
            if count%2 == 0:
                gap = '\n\n'
            else:
                gap = ' : : : : : : '
            message += (team_colors[driver] + driver + gap)
            count += 1
        
        embed = discord.Embed(
            title = ":checkered_flag: Help",
            colour = 0xFF1801,
            description = message
            )
        embed.set_author(
            name = "F1",
            icon_url = "https://1000logos.net/wp-content/uploads/2020/02/F1-Logo.png"
        )
        await ctx.send(embed = embed)


    @commands.command()
    async def predict(self, ctx,  *, prediction):
        prediction = prediction.upper()
        if ',' in prediction:
            predictions = prediction.split(',')
        elif ' ' in prediction:
            predictions = prediction.split(' ')
        else:
            await ctx.send(WRONG_COMMAND_MSG)
            return
        if not self.validatePredictions(predictions):
            await ctx.send(WRONG_COMMAND_MSG)
            return

        with open(F1_PREDICTIONS_LOCATION, 'r') as json_db_read_file:
            json_db = json.load(json_db_read_file)
            json_db_read_file.close()
        json_db = dict(json_db)
        id = str(ctx.author.id)
        json_db[id] = {"name":ctx.author.mention, "predictions":predictions}

        with open(F1_PREDICTIONS_LOCATION, "w") as json_db_write_file:
            json_db_write_file.write(json.dumps(json_db))
            json_db_write_file.close()
    
    @commands.command()
    async def show(self, ctx):
        with open(DRIVERS_COLORS_LOCATION, 'r') as team_colors_file:
            team_colors = json.load(team_colors_file)
            team_colors_file.close()

        message = ""
        with open(F1_PREDICTIONS_LOCATION, 'r') as json_db_read_file:
            json_db = json.load(json_db_read_file)
            json_db_read_file.close()
        if len(json_db) == 0:
            message += 'No predictions'
        else:
            for item in json_db:
                message += (json_db[item]['name'] + ' -> ')
                count = 1
                for driver in json_db[item]['predictions']:
                    if count == 5:
                        gap = ' '
                    else:
                        gap = ' >> '
                    message += (team_colors[driver] + driver + gap)
                    count += 1
                message += '\n\n'

        embed = discord.Embed(
            title = ":checkered_flag: Predictions",
            colour = 0xFF1801,
            description = message
            )
        embed.set_author(
            name = "F1",
            icon_url = "https://1000logos.net/wp-content/uploads/2020/02/F1-Logo.png"
        )
        await ctx.send(embed = embed)

    @commands.command()
    async def results(self, ctx):
        if str(ctx.author.id) == '370440558847590400' or str(ctx.author.id) == '370615332617846786':
            standings = pd.read_csv("./database/winners.txt", sep = "\t",encoding='latin-1')
            standings.drop(['NO','CAR','LAPS','TIME/RETIRED','PTS'], inplace=True,axis=1)

            winnersDict = {}
            for index in standings.index:
                winnersDict[standings['DRIVER'][index]] = standings['POS'][index]

            winnersDict['Kimi Räikkönen'] = winnersDict.pop('Kimi RÃ¤ikkÃ¶nen')
            
        

    @commands.command()
    async def reset(self, ctx):
        if str(ctx.author.id) == '370440558847590400' or str(ctx.author.id) == '370615332617846786':
            with open(F1_PREDICTIONS_LOCATION, "w") as json_db_write_file:
                json_db_write_file.write(json.dumps({}))
                json_db_write_file.close()
            return
        await ctx.send("Not authorized to reset")

        
    def validatePredictions(self, predictions):
        if len(predictions) != 5:
            return False
        for i in range(len(predictions)): 
            predictions[i] = predictions[i].strip()
            if predictions[i] in predictions[:i]:
                return False
            if predictions[i] not in DRIVERS:
                return False
        return True
     

def setup(bot):
    bot.add_cog(f1_pred(bot))