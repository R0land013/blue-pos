import sys
from unittest import TextTestRunner, TestLoader
from tests.settings import set_up, tear_down

test_file_pattern = 'test*.py'

if len(sys.argv) == 2:
    test_file_pattern = 'test*{}*.py'.format(sys.argv[1])

set_up()

test_suite = TestLoader().discover('tests', pattern=test_file_pattern, top_level_dir='.')
runner = TextTestRunner(stream=sys.stdout, verbosity=1)
result = runner.run(test_suite)

tear_down()

sys.exit(len(result.failures))
