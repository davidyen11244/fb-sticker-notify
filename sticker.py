#!/usr/bin/python

import settings
from facebook_helper import FB
import json
import send
import datetime
import codecs

# TODO: make this path as absolute paht
STICKER_FILE = 'stickers'


def main():
    fb = FB(settings.username, settings.password)
    stickers = fb.getStickers()

    # TODO: check if file is exist

    with codecs.open(STICKER_FILE, 'r', 'utf-8') as input:
        content = input.read()
        if content:
            old_stickers = json.loads(content)

            new_stickers = []

            # Check is there any new sticker
            for sticker in stickers:
                isFound = False
                for old_sticker in old_stickers:
                    if sticker['name'].decode('utf-8') == old_sticker['name']:
                        isFound = True
                        break
                if not isFound:
                    new_stickers.append(sticker)

            # If there are new stickers, then notify!
            if new_stickers:
                content = '<ul>\n'
                for new_sticker in new_stickers:
                    content += '<li><p>%s</p><br /><img src=\"%s\"></li><br />\n' % (
                        new_sticker['name'], new_sticker['thumbnail'])
                content += '</ul>'

                today = datetime.date.today().strftime('%m/%d')
                send.sendHtmlEmail(['davidyen1124@gmail.com'],
                                   '[%s] %d New stickers in FB store!' % (
                                       today, len(new_stickers)),
                                   content)

        with open(STICKER_FILE, 'w') as output:
            output.write(json.dumps(stickers, indent=4, ensure_ascii=False))


if __name__ == '__main__':
    main()
