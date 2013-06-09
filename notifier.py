# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import tweepy
from pync import Notifier
import settings


class KeywordListener(tweepy.StreamListener):

    def __init__(self, target_texts, ignore_screen_names=(), *args, **kwargs):
        super(KeywordListener, self).__init__(*args, **kwargs)
        self.notify_name = 'keyword listener'
        self.target_texts = target_texts
        self.ignore_screen_names = ignore_screen_names

    def is_ignore_screen_name(self, screen_name):
        return screen_name in self.ignore_screen_names

    def is_target_text(self, text):
        for target_text in self.target_texts:
            if target_text in text:
                return True
        return False

    def on_status(self, status):
        try:
            text = status.text
            status_id = str(status.id)
            screen_name = status.author.screen_name
        except:
            return

        if self.is_ignore_screen_name(screen_name):
            return
        if not self.is_target_text(text):
            return

        TweetBotStatusNotify(
            text, screen_name, status_id,
            title=self.notify_name,
        )

    def on_error(self, status_code):
        return True

    def on_timeout(self):
        return True


class TweetBotStatusNotify(object):

    base_url = 'tweetbot://%(screen_name)s/status/%(id)s'

    def __init__(self, text, screen_name, status_id, title='TweetBot'):
        url = self.base_url % {'screen_name': screen_name, 'id': status_id}

        Notifier.notify(
            text.encode('utf-8'),
            title=title.encode('utf-8'),
            open=url,
        )


if __name__ == '__main__':
    auth = tweepy.OAuthHandler(settings.consumer_key, settings.consumer_secret)
    auth.set_access_token(settings.access_key, settings.access_secret)
    tweepy.API(auth)

    listener = KeywordListener(
        target_texts=settings.target_texts,
        ignore_screen_names=settings.ignore_screen_names,
    )

    sapi = tweepy.streaming.Stream(auth, listener, secure=True)

    try:
        sapi.userstream()
    except (KeyboardInterrupt, IOError):
        pass
