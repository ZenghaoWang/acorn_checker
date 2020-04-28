import argparse


def get_parser() -> argparse.ArgumentParser:
    '''
    Returns an ArgumentParser. 
    Call its method parse_args() to use.
    '''

    desc = 'Scrapes final marks from Acorn.'
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument(
        '-w', '--winter', help='Scrape marks for winter (Jan - April) semester', action='store_true', default=False)
    parser.add_argument(
        '-f', '--fall', help='Scrape marks for fall (Sept - Dec) semester', action='store_true', default=False)
    parser.add_argument(
        '-s', '--summer', help='Scrape marks for summer (May - August semester)', action='store_true', default=False)
    parser.add_argument(
        '-a', '--all', help='Scrape all marks', action='store_true', default=False)

    return parser
