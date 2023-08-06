import app.sub_task_2.helpers as h


def sub_task_two():
    try:
        title = h.Job(title='Developer')
        title.print_title()
    except Exception as e:
        print(e)


if __name__ == '__main__':
    sub_task_two()
