from django import template

register = template.Library()
@register.filter(name='is_in_cart')
def is_in_cart(product,cart):

      for k,v in cart:
        print("displaying")
        print(k)
        if id==product:
          return True
      return False