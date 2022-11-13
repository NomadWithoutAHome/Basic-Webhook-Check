# version 1.0

import json

import requests as req

# open file and read lines
with open('webhooks.txt', 'r') as f:
    webhooks = f.readlines()

# remove whitespace characters like `\n` at the end of each line
webhooks = [x.strip() for x in webhooks]


# define a function that makes a request and raises an exception
def get_webhook_info(webhook):
    try:
        rep = req.get(webhook, {"name": "application/json"})
        rep.raise_for_status()

        return rep.json()
    except req.exceptions.HTTPError as err:
        pass


# use the function to get the json data from each webhook skipping the invalid ones
for i in range(len(webhooks)):
    webhook_info = get_webhook_info(webhooks[i])

    if webhook_info:
        print(f"Webhook {webhooks[i]} is valid!")
        with open('valid_webhooks.txt', 'a') as f:
            f.write(webhooks[i] + "\n")

        names = [webhook_info['name'] for i, v in enumerate(webhook_info)]
        ids = [webhook_info['id'] for i, v in enumerate(webhook_info)]
        tokens = [webhook_info['token'] for i, v in enumerate(webhook_info)]
        avatars = [webhook_info['avatar'] for i, v in enumerate(webhook_info)]
        channels = [webhook_info['channel_id'] for i, v in enumerate(webhook_info)]
        guilds = [webhook_info['guild_id'] for i, v in enumerate(webhook_info)]

        # put info into a nested dictionary
        valid = {}

        for name, id, token, avatar, channel, guild in zip(names, ids, tokens, avatars, channels, guilds):
            valid = {'Dohm Check': {name: {
                'id': id,
                'token': token,
                'avatar': avatar,
                'channel_id': channel,
                'guild_id': guild,
                'hook_url': 'https://discord.com/api/webhooks/' + id + '/' + token
            }
            }
            }

        print(json.dumps(valid, indent=4))

    else:
        print(f"Webhook {webhooks[i]} is invalid!")

#
# # get json data from each webhook
# for i in webhooks:
#     page = get_webhook_info(i)
#     webhooks.remove(i)
#     print(len(webhooks))
#
#
#
#     names = [page['name'] for i, v in enumerate(page)]
#     ids = [page['id'] for i, v in enumerate(page)]
#     tokens = [page['token'] for i, v in enumerate(page)]
#     avatars = [page['avatar'] for i, v in enumerate(page)]
#     channels = [page['channel_id'] for i, v in enumerate(page)]
#     guilds = [page['guild_id'] for i, v in enumerate(page)]
#
#     # put info into a nested dictionary
#     valid = {}
#
#     for i, v in enumerate(names):
#         valid[names[i]] = {
#             'id': ids[i],
#             'token': tokens[i],
#             'avatar': avatars[i],
#             'channel_id': channels[i],
#             'guild_id': guilds[i]
#         }
#
#     with open('webhooks_info.json', 'w') as f:
#         json.dump(valid, f, indent=4)
