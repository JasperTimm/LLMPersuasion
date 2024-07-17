# LLMPersuasion

This site is a working version of the code required for running a debate with an LLM which attempts to persuade the user to change their mind on a topic. The code is written in Python and uses the Flask web framework to run a web server. The code is designed to be run on a local machine, and the user can interact with the LLM by visiting the web page in a browser.

## Installation

To run the code, you will need to have Python installed on your machine. You can download Python from the official website: https://www.python.org/downloads/

You will also need npm installed on your machine. You can download npm from the official website: https://www.npmjs.com/get-npm

Steps:

1. Clone the repository to your local machine using the following command:

```bash
git clone <repository-url>
```

2. Navigate to the project directory:

```bash
cd LLMPersuasion
```

3. Start a virtual environment:

```bash
python -m venv venv
```

4. Activate the virtual environment:

```bash
source venv/bin/activate
```

5. Install the required Python packages:

```bash
pip install -r requirements.txt
```

6. **In a separate terminal**, navigate to the frontend directory:

```bash
cd debate-frontend
```

7. Install the required npm packages:

```bash
npm install
```

## Usage

The code currently uses OpenAI's API to generate responses from the LLM. To use the code, you will need to set up an OpenAI account and obtain an API key. You can sign up for an account and get an API key from the OpenAI website: https://beta.openai.com/signup/

Once you have obtained an API key, you will need to set it as an environment variable on your machine. You can do this by either creating a `.env` file in the project directory with the following content:

```bash
OPENAI_API_KEY=<your-api-key>
```

Or by setting the environment variable directly in your terminal:

```bash
export OPENAI_API_KEY=<your-api-key>
```

To run the code, you will need to start the Flask web server and the React frontend.

1. In the project directory, start the Flask web server:

```bash
python app.py
```

2. **In a separate terminal**, navigate to the frontend directory:

```bash
cd debate-frontend
```

3. Start the React frontend:

```bash
npm start
```

4. Open a web browser and navigate to the following URL:

```bash
https://localhost:3000/
```

You should now see the debate interface in your web browser. Start a new debate by clicking the "Start Debate" button.

## .env files

The code uses environment variables to store sensitive information such as API keys. These environment variables are stored in `.env` files in the project directory. The `.env` files are not included in the repository for security reasons. You will need to create your own `.env` files with the required environment variables. There is an `.env` file in both the project directory and the frontend directory.

There are template files in the project directory and the frontend directory that you can use to create your own `.env` files. The template files are named `.env.template` and contain the required environment variables. The frontend's `.env.template` file is fine to copy as is (for now), but the project's `.env.template` file will need to be updated with your OpenAI API key and a Flask secret key (can be any random string).

## Accepting self signed certificates in the browser

The site uses a self signed certificate for HTTPS when running locally. This means that the browser will not trust the certificate by default and will show a warning message. To accept the certificate and view the site, you will need to click on the "Advanced" button and then click on the "Proceed to localhost (unsafe)" link.

IMPORTANT: This must be done for BOTH the frontend (https://localhost:3000) and the backend (https://localhost:5000) in order for the site to work correctly.

## Adding users

To add a new user to the site, you can use the following command:

```bash
python add_user.py <username> <password>
```

## Making Changes to models

If you change the models used in models.py, you will usually need to delete the existing DB and create a new one. To do this, you can run the following commands:

```bash
rm instance/debate_website.sqlite
python database.py
```

This will delete the existing database and create a new one with the updated models.

