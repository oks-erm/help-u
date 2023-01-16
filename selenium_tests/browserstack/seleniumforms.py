import os

#######################################################
# configure the environment following instructions on
# https: // www.browserstack.com/
# credentials are included in a submission message
#######################################################


commands = ['browserstack-sdk python3 selenium_tests/comment_test.py',
            'browserstack-sdk python3 selenium_tests/contact_test.py',
            'browserstack-sdk python3 selenium_tests/profile_test.py',
            'browserstack-sdk python3 selenium_tests/signin_test.py',
            'browserstack-sdk python3 selenium_tests/post_test.py',
            'browserstack-sdk python3 selenium_tests/signup_test.py']

for command in commands:
    os.system(command)
