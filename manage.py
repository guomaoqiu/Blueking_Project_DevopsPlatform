import os
import sys

if __name__ == '__main__':
    if 'celery' in sys.argv:
        if 'eventlet' in sys.argv:
            import eventlet
            eventlet.monkey_patch()
        elif 'gevent' in sys.argv:
            from gevent import monkey
            monkey.patch_all()

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
