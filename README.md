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
http://localhost:3000/
```

You should now see the debate interface in your web browser. Start a new debate by clicking the "Start Debate" button.

## Making Changes

If you change the models used in models.py, you will usually need to delete the existing DB and create a new one. To do this, you can run the following commands:

```bash
rm instance/debate_website.sqlite
python database.py
```

This will delete the existing database and create a new one with the updated models.

