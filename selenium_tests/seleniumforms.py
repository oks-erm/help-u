import os

commands = ['browserstack-sdk python3 selenium/comment_test.py',
            'browserstack-sdk python3 selenium/contact_test.py',
            'browserstack-sdk python3 selenium/profile_test.py',
            'browserstack-sdk python3 selenium/signin_test.py',
            'browserstack-sdk python3 selenium/post_test.py',
            'browserstack-sdk python3 selenium/signup_test.py']

for command in commands:
    os.system(command)
