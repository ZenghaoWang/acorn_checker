import argparse


def get_parser() -> argparse.ArgumentParser:
    '''
    Returns an ArgumentParser. 
    Call its method parse_args() to use.
    '''

    desc = 'Scrapes final marks from Acorn. With no flags, the default behavior is to scrape both fall and winter marks.'
    parser = argparse.ArgumentParser(description=desc)
    group = parser.add_mutually_exclusive_group()

    group.add_argument(
        '-w', '--winter', help='Scrape marks for winter (Jan - April) semester', action='store_true')
    group.add_argument(
        '-f', '--fall', help='Scrape marks for fall (Sept - Dec) semester', action='store_true')
    group.add_argument(
        '-s', '--summer', help='Scrape marks for summer (May - August semester)', action='store_true')
    group.add_argument(
        '-a', '--all', help='Scrape all marks', action='store_true')

    group.add_argument(
        '-r', '--reset', help='Reset credentials and exit', action='store_true')

    return parser
