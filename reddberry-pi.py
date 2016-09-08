import praw
import sys
from time import strftime
import datetime

from kivy.config import Config

Config.set('graphics', 'fullscreen', 'auto')

from kivy.app import App
from kivy.uix.scatter import Scatter
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.listview import ListView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock

Config.set('graphics', 'fullscreen', 'auto')

class MainView(GridLayout):
    def __init__(self, **kwargs):
        subreddit = "buildapcsales"
        type = "new"

        r = praw.Reddit(user_agent = 'my_cool_application')

        if type == "new":
            hot = r.get_subreddit(subreddit).get_new(limit = 30)

        elif type == "hot":
            hot = r.get_subreddit(subreddit).get_hot(limit = 30)

        hot = list(hot)

        kwargs['cols'] = 2
        super(MainView, self).__init__(**kwargs)

        # list_view = ListView(item_strings=[str(index) for index in hot])
        layout = GridLayout(
                        cols = 2,
                        spacing=[10, 10],
                        row_force_default=True,
                        row_default_height=75,
                        padding=[10, 10, 10, 10],
                        size_hint_y = None)

        layout.bind(minimum_height=layout.setter('height'))

        def drawRefresh():
            refresh = Button(
                            text = "refresh\nlast refresh - " + strftime("%I:%M:%S"),
                            text_size=(150, 75),
                            valign='middle',
                            size_hint_x=None,
                            width=175,
                            halign='center',
                            font_size=15)

            refresh.bind(on_press=callback)

            layout.add_widget(refresh)
            layout.add_widget(Button(
                                text="/r/" + subreddit + "/" + type,
                                font_size=26,
                                text_size=(1675, 75),
                                halign='left',
                                valign='middle',
                                background_color= (0, 0, 0, 1)))

        # Redraw UI elements
        def callback(instance):
            print("Refreshing..")
            r = praw.Reddit(user_agent = 'my_cool_application')
            if type == "new":
                hot = r.get_subreddit(subreddit).get_new(limit = 30)

            elif type == "hot":
                hot = r.get_subreddit(subreddit).get_hot(limit = 30)
            hot = list(hot)

            layout.clear_widgets()

            drawRefresh()

            for x in hot:
                url = str(x.url)
                url = url.split("//")[1]
                url = url.split("/")[0]

                # Works in /r/news
                if url.startswith("www"):
                    url = url.split(".")[1]
                else:
                    url = url.split(".")[0]

                layout.add_widget(Button(
                                    text=str(x.score) + " votes\n" + str(x.num_comments) + " comments\n" + url,
                                    text_size=(150, 75),
                                    valign='middle',
                                    size_hint_x=None,
                                    width=175,
                                    background_color = (240, 240, 240, .05),
                                    halign='left',
                                    font_size=13))

                layout.add_widget(Button(
                                    text=str(x.title),
                                    font_size=18,
                                    text_size=(1675, 75),
                                    halign='left',
                                    valign='middle',
                                    background_color= (240, 240, 240, .1)))

        refresh = Button(
                        text = "refresh\nlast refresh - " + strftime("%I:%M:%S"),
                        text_size=(150, 75),
                        valign='middle',
                        size_hint_x=None,
                        width=175,
                        halign='center',
                        height=50,
                        font_size=15)

        refresh.bind(on_press=callback)

        layout.add_widget(refresh)
        layout.add_widget(Button(
                            text="/r/" + subreddit + "/" + type,
                            font_size=26,
                            text_size=(1675, 75),
                            halign='left',
                            valign='middle',
                            background_color= (0, 0, 0, 1)))

        for x in hot:
            url = str(x.url)
            url = url.split("//")[1]
            url = url.split("/")[0]

            # Works in /r/news
            if url.startswith("www"):
                url = url.split(".")[1]
            else:
                url = url.split(".")[0]

            layout.add_widget(Button(
                                text=str(x.score) + " votes\n" + str(x.num_comments) + " comments\n" + url,
                                text_size=(150, 75),
                                valign='middle',
                                size_hint_x=None,
                                width=175,
                                background_color = (240, 240, 240, .05),
                                halign='left',
                                font_size=13))

            layout.add_widget(Button(
                                text=str(x.title),
                                font_size=18,
                                text_size=(1675, 75),
                                halign='left',
                                valign='middle',
                                background_color= (240, 240, 240, .1)))


        event = Clock.schedule_interval(callback, 120)

        root = ScrollView()
        root.add_widget(layout)
        self.add_widget(root)

        # self.add_widget(layout)

if __name__ == '__main__':
    from kivy.base import runTouchApp
    runTouchApp(MainView(width = 800))
