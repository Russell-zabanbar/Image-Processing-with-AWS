from django import template
from orders.models import Order, single_order
import queue

register = template.Library()


@register.inclusion_tag('orders/inclusion_queue.html')
def queue_list(is_baker):
    numbers = Order.objects.all()
    ones = single_order.objects.all()
    numbers_queue = queue.Queue()
    ones_queue = queue.Queue()

    for num in numbers:
        numbers_queue.put(num)

    for one in ones:
        ones_queue.put(one)

    nums_and_ones = queue.Queue()
    while True:
        if not numbers_queue.empty():
            nums_and_ones.put(numbers_queue.get())
        if not ones_queue.empty():
            nums_and_ones.put(ones_queue.get())

        if numbers_queue.empty() and ones_queue.empty():
            break

    nums_and_ones_list = list(nums_and_ones.queue)
    print(nums_and_ones_list)

    if is_baker:
        return {'nums_and_ones': nums_and_ones_list, 'is_baker': True}
    else:
        return {'nums_and_ones': nums_and_ones_list, 'is_baker': False}
