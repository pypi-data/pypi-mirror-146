import sub_task_1.sub_task_1 as s_one
import sub_task_2.sub_task_2 as s_two


def main():
    try:
        s_one.sub_task_one()
        s_two.sub_task_two()
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()

