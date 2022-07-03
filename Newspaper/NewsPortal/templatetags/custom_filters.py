from django import template

register = template.Library()

CURRENCIES_SYMBOLS = {
   'rub': '₽',
   'usd': '$',
}

@register.filter()
def currency(value, code='rub'):
   postfix = CURRENCIES_SYMBOLS[code]
   return f'{value} {postfix}'

@register.filter()
def censor(value):
   for i in curselist:
      if i.find(value):
         value = value.replace(i[1:-1], "*" * (len(i)-2))
      else:
         return f'{value}'
   return f'{value}'

@register.filter(name='update_page')
def update_page(full_path:str, page:int):
    try:
        params_list = full_path.split('?')[1].split('&')
        params = dict([tuple(str(param).split('=')) for param  in params_list])
        params.update({'page' : page})
        link = ''
        for key, value in params.items():
            link += (f"{key}={value}&")
        return link[:-1]
    except:
        return f"page={page}"

curselist =[
   'блядки',
   'блядовать',
   'блядство',
   'блядь',
   'блять',
   'бугор',
   'в пизду',
   'встать раком',
   'выёбываться',
   'гандон',
   'говно',
   'говнюк',
   'дать пизды',
   'дерьмо',
   'дрочить',
   'ёбарь',
   'ебать',
   'ебать',
   'ебло',
   'ебнуть',
   'ёб твою мать',
   'жопа',
   'жополиз',
   'манда',
   'мандавошка',
   'мудак',
   'мудила',
   'мудозвон',
   'наебать',
   'наебениться',
   'наебнуться',
   'нахуй',
   'нахуя',
   'нахуячиться',
   'нихуя',
   'охуеть',
   'охуительно',
   'сиськи',
   'спиздить',
   'срать',
   'ссать',
   'траxать',
   'хуёво',
   'хуёвый',
   'хуеплет',
   'хуйло',
   'хуйней страдать',
   'хуйня',
   'хуй',
   'хуйнуть',
   'хуй пинать'
]