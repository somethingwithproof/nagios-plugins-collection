# XML URL Checker

This script checks if an XML document at a specified URL contains the "reservedPrefixes" element. It performs the following checks:

1. It connects to the specified URL and retrieves the XML content.
2. It parses the XML document and checks if the "reservedPrefixes" element is present.
3. If the element is found, it prints a success message.
4. If the element is not found or if there are any errors during the process, it raises appropriate exceptions.

## Prerequisites

- Python 2.x or 3.x

## Usage

Run the script with the URL as a command-line argument:

```shell
python main.py YOUR_URL
```
Replace YOUR_URL with the actual URL you want to check.

## Example

```shell
python main.py http://example.com/data.xml
```

## License

This project is licensed under the MIT License.

Feel free to modify the content or structure of the `README.md` file as needed.




