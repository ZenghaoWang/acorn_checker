from argparse import ArgumentParser


def get_parser() -> ArgumentParser:
    '''
    Returns an ArgumentParser. 
    Call its method parse_args() to use.
    '''

    desc = 'Scrapes final marks from Acorn. With no flags, the default behavior is to scrape both fall and winter marks.\n Use -p flag to scrape published courses from quercus instead.'
    parser: ArgumentParser = ArgumentParser(description=desc)
    semester = parser.add_mutually_exclusive_group()
    options = parser.add_mutually_exclusive_group()

    semester.add_argument(
        '-w', '--winter', help='Scrape marks for winter (Jan - April) semester', action='store_true')
    semester.add_argument(
        '-f', '--fall', help='Scrape marks for fall (Sept - Dec) semester', action='store_true')
    semester.add_argument(
        '-s', '--summer', help='Scrape marks for summer (May - August semester)', action='store_true')
    semester.add_argument(
        '-a', '--all', help='Scrape all marks', action='store_true')

    options.add_argument(
        '-r', '--reset', help='Reset credentials and exit', action='store_true')
    options.add_argument(
        '-c', '--config', help='Configure default behavior when no flags are used', action='store_true')
    options.add_argument(
        '-p', '--published', help='View list of published courses on quercus', action='store_true')

    return parser
