import samino
import time
import re

email = ""
password = ""
banwords = ["shit"]
rejoin = False
client = samino.Client()
client.login(email, password, socket=True)


def replacer(string):
    return string.replace("'", "").replace("/", "").replace('"',"").replace("*","").replace(".", "").replace(",","").replace("+","").replace("×","").replace("÷","").replace("=","").replace("_", "").replace("€", "").replace("£","").replace("¥", "").replace("₩", "").replace("!", "@").replace("#", "").replace("$", "%").replace("^", "").replace("&", "").replace("(", "").replace(")", "").replace("-", "").replace(":", "").replace(";", "").replace("`", "").replace("~", "").replace("\\", "").replace("|", "").replace("<", "").replace(">", "").replace("{", "").replace("}", "").replace("[", "").replace("]", "").replace("°", "").replace("•", "").replace("○", "").replace("●", "").replace("□", "").replace("■", "").replace("♤", "").replace("♡", "").replace("◇", "").replace("♧", "").replace("☆", "").replace("▪︎", "").replace("¤", "").replace("《", "").replace("》", "").replace("¡", "").replace("¿", "").replace("،", "").replace("؟", "").replace("!","").replace("َ", "").replace("ً", "").replace("ُ", "").replace("ٌ", "").replace("ْ", "").replace("ِ", "").replace("ٍ", "").replace("ّ", "").replace(" َ", "").replace(" ٕ", "").replace("ـ", "").replace(" ُ", "").replace(" ِ", "").replace("ٓ", "").replace(" ٰ", "").replace("ٖ", "").replace(" ً", "").replace(" ّ", "").replace("ٌ", "").replace(" ٍ", "").replace(" ْ", "").replace("ٔ", "").replace("%", "").replace("&", "")


@client.event("on_video_chat_start")
@client.event("on_avatar_chat_end")
@client.event("on_video_chat_end")
@client.event("on_voice_chat_end")
@client.event("on_avatar_chat_start")
@client.event("on_screen_room_start")
@client.event("on_screen_room_end")
def on_ghost_messages(data: samino.lib.Event):
    author = data.message.author
    chatId = data.message.chatId
    local = samino.Local(data.comId)
    counter = 0

    with open("ghost_spam.txt", "r+") as file:
        for line in file:
            if line.strip("\n") == author.userId:
                counter += 1

        if author.userId != client.uid: file.writelines(f"{str(author.userId)}\n")
        if counter > 3: local.kick(chatId, author.userId, rejoin)
        hosts = [local.get_chat_info(chatId).author.userId]
        hosts.extend(local.get_chat_info(chatId).coHosts)
        if author.userId not in local.get_chat_info(chatId).coHosts: local.kick(chatId, author.userId, rejoin)


@client.event("on_text_message")
@client.event("on_sticker_message")
@client.event("on_image_message")
@client.event("on_voice_message")
def on_messages(data: samino.lib.Event):
    author = data.message.author
    chatId = data.message.chatId
    local = samino.Local(data.comId)
    counter = 0

    if len(re.findall(r'(https?://[^\s]+)', data.message.content)) > 0: local.kick(chatId, author.userId, rejoin)

    for word in replacer(data.message.content.split(" ")):
        if word in banwords: local.kick(chatId, author.userId, rejoin)

    with open("text_spam.txt", "r+") as file:
        for line in file:
            if line.strip("\n") == author.userId:
                counter += 1
        if author.userId != client.uid: file.writelines(f"{str(author.userId)}\n")
        if counter > 3: local.kick(chatId, author.userId, rejoin)


@client.event("on_group_member_join")
@client.event("on_group_member_leave")
def on_members(data: samino.lib.Event):
    counter = 0
    chatId = data.message.chatId
    userId = data.json["chatMessage"]["uid"]
    local = samino.Local(data.comId)

    with open("member_spam.txt", "r+") as file:
        for line in file:
            if line.strip("\n") == userId:
                counter += 1

        if userId != client.uid: file.writelines(f"{str(userId)}\n")
        if counter > 3: local.kick(chatId, userId, rejoin)


def task():
    print("ready!")
    while True:
        with open("ghost_spam.txt", "w") as f: f.truncate(0)
        with open("text_spam.txt", "w") as f: f.truncate(0)
        with open("member_spam.txt", "w") as f: f.truncate(0)
        time.sleep(10)


if __name__ == "__main__":
    task()
