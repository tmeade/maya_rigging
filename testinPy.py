import logging

logging.basicConfig(level=logging.INFO)

def print_test (input):
    input = input
    logging.info('hello %d' % input)


print_test(5)
