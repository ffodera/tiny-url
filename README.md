# Example tiny-url generator
This repository is an example of using python to create a web application that shortens URLs and redirects them when 
accessed.

## Requirements
- Flask - 0.12.2
- sqlite3 - 3.20.1
- Python - 2.7.14
- Bootstrap - 3.3.7

## Running the server
This code was tested and built on Fedora 27, kernel 4.14.11 that contains an internet connection. The instructions are 
based on a Fedora based Linux environment and may require slight modifications in other environments.

### Steps:
1. Clone the repository:

    `git clone https://github.com/ffodera/tiny-url.git`
2. Install sqlite to the host OS:

    `dnf install sqlite` 
    
3. Install Flask to the host OS:

    `pip install flask`
    
4. Under the cloned directory run the following command to verify the database file is created:

    `sqlite3 url_links.db`
    
5. Open a new terminal window to the cloned directory and run the main application:

    `./tiny_url.py` OR `python tiny_url.py`
    
6. In a browser navigate to the home page:

    `http://localhost:8000`
    
7. Enter a URL that you want to shorten, hit `Submit`

8. Copy the URL that was generated! Enjoy!