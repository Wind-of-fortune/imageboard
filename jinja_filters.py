def format_date(date_x):
    date_x = str(date_x)
    new_date = date_x[8:10] + '.' + date_x[5:7] + '.' + date_x[0:4]
    return new_date


def format_head(h):
    h = str(h)
    miss = 60 - len(h)
    new_h = h + ' '*miss
    return new_h


def format_text_art(some_text):
    string = ''
    num = 0
    for i in range (len(some_text)):
        num += 1
        string += some_text[i]
        if num > 100:
            if some_text[i] == ' ':
                string += '\n'
                num = 0
    return string


def format_text_comments(some_text):
    string = ''
    num = 0
    for i in range (len(some_text)):
        num += 1
        string += some_text[i]
        if num > 40:
            if some_text[i] == ' ':
                string += '\n'
                num = 0
            if num > 45:
                string += '\n'
                num = 0
    return string


