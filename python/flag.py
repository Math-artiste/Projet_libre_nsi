import random
import csv

        # if response == 'next':
        #     with open(r'csv_files/flag.csv', mode='r') as csv_file:
        #         csv_reader = csv.DictReader(csv_file)
        #         randomResult = random.randint(1, 258)
        #         # On évite les répétitions
        #         while str(randomResult) == self.question_used:
        #             randomResult = random.randint(1, 31)
        #         randomFaux1 = random.randint(1, 258)
        #         if randomFaux1 == randomResult:
        #             randomFaux1 = random.randint(1, 258)
        #         randomFaux2 = random.randint(1, 258)
        #         if randomFaux2 == randomResult or randomFaux2 == randomFaux1:
        #             randomFaux2 = random.randint(1, 258)
        #         randomFaux3 = random.randint(1, 258)
        #         if randomFaux3 == randomResult or randomFaux3 == randomFaux1 or randomFaux3 == randomFaux2:
        #             randomFaux3 = random.randint(1, 258)
        #         line = 0
        #         for row in csv_reader:
        #             if line == randomResult:
        #                 flag = f"https://flagcdn.com/256x192/{row['shortname']}.png"
        #                 realFlagName = row['realname']
        #             elif line == randomFaux1:
        #                 falseflagName1 = row['realname']
        #             elif line == randomFaux2:
        #                 falseflagName2 = row['realname']
        #             elif line == randomFaux3:
        #                 falseflagName3 = row['realname']
        #             line += 1
        #         allFlagsNames = [realFlagName, falseflagName1,
        #                         falseflagName2, falseflagName3]
        #         flagsOrder = random.sample(allFlagsNames, len(allFlagsNames))
        #         self.tourCounter += 1
        #         self.question_used.append(str(randomResult))
        #         embed = discord.Embed(title=f"Flag Quizz   ```{self.tourCounter - self.errorCounter} sur {self.tourCounter}```").set_image(url=flag)
        #         await interaction.response.edit_message(view=flagView(self.userId, realFlagName, flagsOrder, embed, self.errorCounter, self.tourCounter, self.avatar, self.question_used), embed=embed)
        # count = 0
        # if response == self.realFlagName:
        #     self.bon = True
        #     for x in self.flagsOrder:
        #         if str(response) == str(x):
        #             self.add_item(discord.ui.Button(
        #                 style=discord.ButtonStyle.green, label=self.flagsOrder[count], custom_id=self.flagsOrder[count], disabled=True))
        #             self.add_item(discord.ui.Button(
        #                 style=discord.ButtonStyle.primary, label='Next', custom_id='next', row=2))
        #             self.add_item(discord.ui.Button(
        #                 style=discord.ButtonStyle.red, label='Stop', custom_id='stop', row=2))
        #         else:
        #             self.add_item(discord.ui.Button(
        #                 style=discord.ButtonStyle.blurple, label=self.flagsOrder[count], custom_id=self.flagsOrder[count], disabled=True))
        #         count += 1
        # else:
        #     if self.bon is True:
        #         self.errorCounter += 1
        #         self.bon = False
        #     for x in self.flagsOrder:
        #         if str(response) == str(x):
        #             self.add_item(discord.ui.Button(
        #                 style=discord.ButtonStyle.red, label=self.flagsOrder[count], custom_id=self.flagsOrder[count]))
        #         else:
        #             self.add_item(discord.ui.Button(
        #                 style=discord.ButtonStyle.blurple, label=self.flagsOrder[count], custom_id=self.flagsOrder[count]))
        #         count += 1
        # await interaction.response.edit_message(view=self, embed=self.embed)


def get_flag():
    with open(r'csv_files/flag.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        randomResult = random.randint(1, 258)
        randomFaux1 = random.randint(1, 258)
        if randomFaux1 == randomResult:
            randomFaux1 = random.randint(1, 258)
        randomFaux2 = random.randint(1, 258)
        if randomFaux2 == randomResult or randomFaux2 == randomFaux1:
            randomFaux2 = random.randint(1, 258)
        randomFaux3 = random.randint(1, 258)
        if randomFaux3 == randomResult or randomFaux3 == randomFaux1 or randomFaux3 == randomFaux2:
            randomFaux3 = random.randint(1, 258)
        line = 0
        for row in csv_reader:
            if line == randomResult:
                flag = f"https://flagcdn.com/256x192/{row['shortname']}.png"
                realFlagName = row['realname']
            elif line == randomFaux1:
                falseflagName1 = row['realname']
            elif line == randomFaux2:
                falseflagName2 = row['realname']
            elif line == randomFaux3:
                falseflagName3 = row['realname']
            line += 1
        allFlagsNames = [realFlagName, falseflagName1,
                         falseflagName2, falseflagName3]
        return flag, allFlagsNames, allFlagsNames[0].lower().replace(" ","")