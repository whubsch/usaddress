# usaddress

usaddress is a Python library for parsing unstructured United States address strings into address components, using advanced NLP methods.

> [!NOTE]
> This repository is a fork of the [usaddress library](https://github.com/datamade/usaddress) that was created by [datamade](https://github.com/datamade). This fork seeks to update usaddress to be more efficient and officially compatible with current Python versions.

**What this can do:** Using a probabilistic model, it makes (very educated) guesses in identifying address components, even in tricky cases where rule-based parsers typically break down.

**What this cannot do:** It cannot identify address components with perfect accuracy, nor can it verify that a given address is correct/valid.

## How to use the usaddress python library

1. Install usaddress with [pip](https://pip.readthedocs.io/en/latest/quickstart.html).

In the terminal,

```bash
pip install git+https://github.com/whubsch/usaddress.git
```

2. Parse some addresses!

Note that `parse` and `tag` are different methods:

```python
import usaddress
addr='123 Main St. Suite 100 Chicago, IL'

# The parse method will split your address string into components, and label each component.
usaddress.parse(addr)
# [('123', 'AddressNumber'), ('Main', 'StreetName'), ('St.', 'StreetNamePostType'), ('Suite', 'OccupancyType'), ('100', 'OccupancyIdentifier'), ('Chicago,', 'PlaceName'), ('IL', 'StateName')]

# The tag method will try to be a little smarter; it will merge consecutive components, strip commas, & return an address type
usaddress.tag(addr)
# ({'AddressNumber': '123', 'StreetName': 'Main', 'StreetNamePostType': 'St.', 'OccupancyType': 'Suite', 'OccupancyIdentifier': '100', 'PlaceName': 'Chicago', 'StateName': 'IL'}, 'Street Address')

```

## How to use this development code (for the nerds)

usaddress uses [parserator](https://github.com/datamade/parserator), a library for making and improving probabilistic parsers - specifically, parsers that use [python-crfsuite](https://github.com/tpeng/python-crfsuite)'s implementation of conditional random fields. Parserator allows you to train the usaddress parser's model (a .crfsuite settings file) on labeled training data, and provides tools for adding new labeled training data.

### Building & testing the code in this repo

To build a development version of usaddress on your machine, run the following code in your command line:

```
git clone https://github.com/whubsch/usaddress.git
cd usaddress
pip install -r requirements.txt
python setup.py develop
parserator train training/labeled.xml usaddress
```

Then run the testing suite to confirm that everything is working properly:

```
nosetests .
```

Having trouble building the code? [Open an issue](https://github.com/whubsch/usaddress/issues/new) and we'd be glad to help you troubleshoot.

### Adding new training data

If usaddress is consistently failing on particular address patterns, you can adjust the parser's behavior by adding new training data to the model. [Follow our guide in the training directory](https://github.com/whubsch/usaddress/blob/master/training/README.md), and be sure to make a pull request so that we can incorporate your contribution into our next release!

## Important links

- Repository: https://github.com/whubsch/usaddress
- Issues: https://github.com/whubsch/usaddress/issues

## Bad Parses / Bugs

Report issues in the [issue tracker](https://github.com/whubsch/usaddress/issues)

If something in the library is not behaving intuitively, it might be a bug, and should be reported.

## Note on Patches/Pull Requests

- Fork the project.
- Make your feature addition or bug fix.
- Send us a pull request. Bonus points for topic branches!

## License

[MIT](https://github.com/whubsch/usaddress/blob/master/LICENSE)
