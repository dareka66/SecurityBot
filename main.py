import samino
import time

email = ""
password = ""
client = samino.Client()
client.login(email, password)

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
        for line in file.read().splitlines():
            if line == author.userId:
                counter += 1

        if author.userId != client.uid: file.writelines(f"{str(author.userId)}\n")
        elif counter > 4: local.kick(chatId, author.userId, False)


@client.event("on_text_message")
@client.event("on_sticker_message")
@client.event("on_image_message")
@client.event("on_voice_message")
def on_messages(data: samino.lib.Event):
    author = data.message.author
    chatId = data.message.chatId
    local = samino.Local(data.comId)
    counter = 0

    with open("text_spam.txt", "r+") as file:
        for line in file.read().splitlines():
            if line == author.userId:
                counter += 1

        if author.userId != client.uid: file.writelines(f"{str(author.userId)}\n")
        elif counter > 4: local.kick(chatId, author.userId, False)


@client.event("on_group_member_join")
@client.event("on_group_member_leave")
def on_members(data: samino.lib.Event):
    counter = 0
    chatId = data.message.chatId
    userId = data.json["chatMessage"]["uid"]
    local = samino.Local(data.comId)

    with open("member_spam.txt", "r+") as file:
        for line in file.read().splitlines():
            if line == userId:
                counter += 1

        if userId != client.uid: file.writelines(f"{str(userId)}\n")
        if counter > 5: local.kick(chatId, userId, False)


def task():
    print("ready!")
    while True:
        with open("ghost_spam.txt", "w") as f: f.truncate(0)
        with open("text_spam.txt", "w") as f: f.truncate(0)
        with open("member_spam.txt", "w") as f: f.truncate(0)
        time.sleep(10)


if __name__ == "__main__":
    task()
