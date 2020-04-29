# Sample Text

A simple command-line application which scrapes final marks off of acorn. Credentials are stored locally inside config.json.

## Installation

Download repository:

```bash
git clone https://github.com/ZenghaoWang/acorn_checker
```

Install dependencies:

```bash
python3 -m pip install -r requirements.txt
```

Install [Chrome WebDriver](https://chromedriver.chromium.org/downloads) and add to PATH

## Usage

Navigate to repo folder and run program

```bash
python3 main.py
python3 main.py -h # Help
python3 main.py -f # Show fall marks
python3 main.py -w # Show winter marks
python3 main.py -a # Show all marks
python3 main.py -r # Reset credentials
python3 main.py -c # Config default no-flag behavior
```

### Published courses

Use the -p flag to instead output a list of course pages that have been published for a given semester.

```bash
python3 main.py -p # Returns all published course pages
python3 main.py -p -s # Returns all published summer course pages
```

## Disclaimer

I'm not responsible if you violate acorn TOS while using this.

## License

This project is licensed under the MIT license - See [LICENSE.md](https://github.com/ZenghaoWang/acorn_checker/blob/master/LICENSE.md) for details.
