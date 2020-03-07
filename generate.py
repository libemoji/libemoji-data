#!/usr/bin/python3

import json
import re
import sys
import urllib.request


def slug(text):
    return re.sub(r'[\ \&]+', '-', text.lower())


def unslug(text):
    return text.replace('-', ' ').capitalize()


output = {'groups': [], 'emojis': []}
url = 'https://unicode.org/Public/emoji/13.0/emoji-test.txt'
#urllib.request.urlretrieve(url, 'emoji-test.txt')

with open('emoji-test.txt', 'r') as data_file:

    lines = data_file.readlines()
    for line in lines:
        line = line[0:-1]
        if line.startswith('# group: '):
            group_name = line[9:]
            group_id = slug(group_name)
            output['groups'].append({
                'id': group_id,
                'name': group_name,
            })

        elif line.startswith('# subgroup: '):
            subgroup_id = line[12:]
            subgroup_name = unslug(subgroup_id)
            output['groups'].append({
                'id': subgroup_id,
                'name': subgroup_name,
                'parent': group_id,
            })
        elif not line.startswith('#') and len(line) > 10:
            code = line[0:42].strip().split(' ')
            length = len(code)
            emoji = {
                'chars': line[67:67+length],
                'codes': code,
                'status': line[45:65].strip(),
                'since': float(line[69+length:73+length].strip()),
                'name': line[73+length:].strip(),
            }
            output['emojis'].append(emoji)

with open('emoji-data.json', 'w') as json_file:
    json_file.write(json.dumps(output, indent=2, separators=(',', ': ')))

with open('emoji-data.xml', 'w') as xml_file:
    xml = '<?xml version="1.0" encoding="UTF-8" ?>\n<emojidata>\n  <groups>\n'
    for group in output['groups']:
        xml += '    <group id="' + \
            group['id'] + '" name="' + \
            group['name'].replace('&', '&amp;') + '"'
        if 'parent' in group:
            xml += ' parent="' + group['parent'] + '"'
        xml += '/>\n'
    xml = '  </groups>\n  <emojis>\n'
    for emoji in output['emojis']:
        xml += '    <emoji chars="' + emoji['chars'] + '" codes="' + \
            ' '.join(emoji['codes']) + '" status="' + emoji['status'] + \
            '" since="' + str(emoji['since']) + \
            '" name="' + emoji['name'] + '"/>\n'
    xml += '  </emojis>\n</emojidata>\n'
    xml_file.write(xml)
