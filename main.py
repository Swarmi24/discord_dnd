from random import randint
from discord.ext import commands
import sqlite3


class DB:
    def __init__(self):
        try:
            self.conn = sqlite3.connect('dnd.sqlite')
            self.cur = self.conn.cursor()
        except sqlite3.Error as e:
            print(e)

    def create_tables(self):
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS users(
                id INT PRIMARY KEY,
                username TEXT UNIQUE,
                race TEXT,
                strong INTEGER
            )
        """)
        self.conn.commit()

    def get(self, query):
        self.cur.execute(query)
        return self.cur.fetchall()

    def first(self, query):
        print(query)
        self.cur.execute(query)
        return self.cur.fetchone()

    def insert(self, query, values):
        self.cur.execute(query, values)
        self.conn.commit()
        return True


class User:
    def __init__(self, username, race, strong):
        self.username = str(username)
        self.race = str(race)
        self.strong = str(strong)
        self.db = DB()

    def create(self):
        self.db.insert("INSERT INTO users (username, race, strong) VALUES (?, ?, ?)", (self.username, self.race, self.strong))
        result = self.db.first("SELECT username, race, strong FROM users WHERE username = '" + self.username + "'")
        answer = """
            username: {0},
            race: {1},
            strong: {2},
        """.format(result[0], result[1], result[2])
        return answer

    def first(self):
        result = self.db.first("SELECT username, race, strong FROM users WHERE username = '" + self.username + "'")
        return result


d = DB()
d.create_tables()
# Токен бота с https://discord.com/developers
TOKEN = 'ODQwODQ1NjE3ODExMDMwMDM2.YJeIgQ.tVbVnBxAZz5qUyCe_to_G7_eu8Y'

bot = commands.Bot(command_prefix='!')



@bot.command(pass_context=True)
async def user(ctx, race=None, strong=None):
    if (race and strong):
        user = User(ctx.message.author.name, race, strong)
        result = user.create()
    else:
        result = "заполняй блядь поля, я че их высрать должен!!!!"
    await ctx.send(result)


@bot.command(pass_context=True)
async def д(ctx, d_type, n=1):
    author = ctx.message.author.name
    result = ""
    sum = 0
    for i in range(n):
        numb = randint(1, int(d_type))
        if i != n - 1:
            result = result + " {0},".format(numb)
        else:
            result = result + " {0}".format(numb)
        sum = sum + numb
    await ctx.send("{0} выбрасывает: {2} \nСумма {3}".format(author, d_type, result, sum))


# Пример отправки сообщения
@bot.command(pass_context=True)
async def test(ctx):
    await ctx.send(ctx.message)


# Пример с озвучкой и emoji
@bot.command(pass_context=True)
async def ваня(ctx):
    await ctx.send("Ваня = <:chickenVanya:841186571058937876>")
    await ctx.send("vanya huueesos", tts=True)

bot.run(TOKEN)