from app.sub_task_1 import helpers as h


def sub_task_one():
    try:
        person = h.Person(name='Nick')
        person.print_name()
    except Exception as e:
        print(e)


if __name__ == '__main__':
    sub_task_one()
