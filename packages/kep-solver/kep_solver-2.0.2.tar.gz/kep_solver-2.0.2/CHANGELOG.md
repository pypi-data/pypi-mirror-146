# Changelog


## [Unreleased]

- Rework UK backarcs. To match existing code, these are implemented in a
	specific manner.
- Alternate and embedded exchanges for cycles must be cycles, and alternate and
	embedded exchanges for chains must be chains that use the same non-directed
	donor
- Add __repr__ to Donor

## [2.0.0]

- New class for Exchange objects
- Add build\_alternates\_and\_embeds() function to find alternate and embedded
	cycles
- Update documentation to add example of CompatibiltyGraph usage
- Moved to [Black](https://black.readthedocs.io/en/stable/) for formatting

## [1.0.4]

- Use setuptools\_scm for versioning

## [1.0.3]

- Fix continuous deployment

## [1.0.2]

- Fix documentation

## [1.0.1]

- Add ability to read blood groups of donors and recipients
- Add Recipient.pairedWith(Donor) function
- Add custom exceptions for data IO
- Allow variations of bloodgroup/bloodtype in input
- Allow variations of cPRA/PRA/cpra in input
- Add functions for blood group compatibility checks to Donor and Recipient

## [1.0.0]

First release
