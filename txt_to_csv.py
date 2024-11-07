import json
import csv
import re

field_name = ['category','id1','utterance1','id2','utterance2','agreement','laugh']

current_data = {'category':None, 'id1':None, 'utterance1':None, 'id2':None, 'utterance2':None, 'agreement':None, 'laugh':None}

data =[]

def category_judge(line, category):
    if line[0] == '＠':
        if line[1:] == 'ＥＮＤ\n':
            return category
        else:
            return int(line[1:])
    else:
        return category
    
def judge(line):
    if line[0] == '＠':
        if line[1:] == 'ＥＮＤ\n':
            return False
        else:
            return True
    else:
        return True
    
def id_judge(line):
    if '：' in line:
        if '％ｃｏｍ' in line:
            return 0
        else:
            return 1
    else:
        return 2
        
def utterance(line):
    if ':' in line:
        id, utterance = line.split('：')
        return id, utterance
    else:
        return line
    
def cleansing(line, speaker1, speaker2):
    pattern = re.compile(r"（.*?）|＜.*?＞|＊|【.*?】")
    pat1 = re.compile(r'{0}'.format(speaker1))
    pat2 = re.compile(r'{0}'.format(speaker2))
    line = pattern.sub('', line)
    line = pat1.sub('', line)
    line = pat2.sub('', line)
    return line

# def agreement(line):

speaker1 = 'F011'
speaker2 = 'F089'
previous_id = None
current_id = None
current_line = ''

with open('/nucc_csvdata/data007_1.csv','w',encoding='utf-8') as csvfile:
    with open('/nucc_relationship/data007_1.txt', 'r') as in_file:
        for line in in_file:
            current_data['category'] = category_judge(line, current_data['category'])
            print(line)
            print('b')
            if judge(line) == False:
                current_data['id1'] = current_data['id2']
                current_data['utterance1'] = current_data['utterance2']
                current_data['id2'] = current_id
                current_data['utterance2'] = current_line
                print('c')
                if current_data['id1'] is not None and current_data['id2'] is not None and current_data['id1'] != current_data['id2']:
                        data.append(current_data.copy())
                        print('goal')
                break
            else:
                print('d')
                if id_judge(line) == 1:
                    current_data['id1'] = current_data['id2']
                    current_data['utterance1'] = current_data['utterance2']
                    current_data['id2'] = current_id
                    current_data['utterance2'] = current_line
                    previous_id = current_id
                    current_id, current_line = line.split('：')
                    current_line = cleansing(current_line, speaker1, speaker2)
                    print(current_data)
                    print('a')
                    if current_data['id1'] is not None and current_data['id2'] is not None and current_data['id1'] != current_data['id2']:
                        data.append(current_data.copy())
                        print('goal')
                elif id_judge(line) == 2:
                    current_line += cleansing(line, speaker1, speaker2)
                    print('aiueo')
                    print(current_line)
                elif id_judge(line) == 0:
                    line = ''

                                
    writer = csv.DictWriter(csvfile, fieldnames = field_name)
    writer.writeheader()
    writer.writerows(data)