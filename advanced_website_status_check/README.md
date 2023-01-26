# Website Status Checker

A Python script that checks the status of a website or server at a specified URL. The script exits with a status code of 0 if the response is successful, or 2 if there is an error.

## Getting Started

The script requires Python 3 and the following libraries:

`httpx`

To use the script, simply run the command python main.py URL, where URL is the website or server you want to check.

### **Input Validation**

The script checks if the user has provided a URL as a command line argument. If no argument is provided, the script will display the usage instructions and exit. The script also checks if the URL provided starts with "http" or "https", and if not, it will add "http://" to the URL before making the request.

### **Output Format**

The script prints the status of the check and the time it was performed in the following format:

