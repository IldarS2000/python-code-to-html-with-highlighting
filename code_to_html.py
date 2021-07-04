import keyword
import builtins
import re


def add_html_tag_with_head(lang='en', title='title'):
    def decorator(func):
        def wrapper(code):
            html = f"""
<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<title>{title}</title>
<link rel="stylesheet" href="styles.css">
</head>\n"""

            code = func(code)
            html = f'{html}\n{code}\n</html>'
            return html

        return wrapper

    return decorator


def add_tag(tag):
    def decorator(func):
        def wrapper(code):
            code = func(code)
            html = f'<{tag}>\n{code}\n</{tag}>'
            return html

        return wrapper

    return decorator


def add_spans(func):
    keywords = keyword.kwlist

    keywords = {f'{kword}': fr'<span class="keyword">{kword}</span>' for kword in keywords}
    embedded = dir(builtins)
    embedded = {f'{emb}': fr'<span class="builtin">{emb}</span>' for emb in embedded}

    def wrapper(code: str):
        html = func(code)

        # обрамляем отдельно слово класс
        html = re.sub(r'\bclass\b', keywords['class'], html)
        keywords.pop('class')

        # обрамляем литералы чисел
        html = re.sub(r'\b([\d]+[\.]?[\d]*)\b', r'<span class="literal">\1</span>', html)

        # обрамляем строки
        html = re.sub(r'[\'](.+?)[\']', r"""<span style="color:#678050;">'\1'</span>""", html)

        # обрамляем функции
        html = re.sub(r'\b(def)\b \b([_a-zA-Z][\w]*)\b', r'def <span class="function">\2</span>', html)

        # обрамляем ключевые слова
        for kword, spanned_keyword in keywords.items():
            html = re.sub(fr'\b{kword}\b', spanned_keyword, html)

        # обрамляем встроенные обьекты
        for emb, spanned_emb in embedded.items():
            html = re.sub(fr'\b{emb}\b', spanned_emb, html)
        return html

    return wrapper


def add_blank_spaces(func):
    def wrapper(code: str):
        code = func(code)

        html = ' '

        flag = True
        for symbol in code:
            if symbol == ' ' and flag:
                html += '&nbsp;'
            elif symbol == '\n':
                html += '<br>'
                flag = True
            else:
                html += symbol
                flag = False

        return html

    return wrapper


@add_html_tag_with_head(title='code')
@add_tag('body')
@add_tag('p')
@add_spans
@add_blank_spaces
def get_html(code: str):
    return code


def main():
    with open('pycode.txt', 'r') as file:
        code = file.read()
    code = get_html(code)
    with open('pycode.html', 'w') as file:
        file.write(code)


if __name__ == '__main__':
    main()
