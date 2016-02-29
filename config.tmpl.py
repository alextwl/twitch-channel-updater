'''
Template of config.py

hard-coded for testing purpose, should be removed later.
'''

tokens = {
    "access_token": "",
    "refresh_token": "",
    "scope": ["user_read", "channel_read", "channel_editor", "chat_login"],
    "token_type": ""
    }

# after we can get channel apis from twitch kraken root by js,
# user_read is no longer needed and we can get rid of it.
# im sick of dealing with privacy issue. better not to touch it.
