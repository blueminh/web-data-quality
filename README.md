## Backend
The backend is implemented using Flask. The flask server runs on port 8085

### Prerequisites

Before running the project, ensure you have the following prerequisites installed:

- [Python 3.9+](https://www.python.org/downloads/release/python-390/)
- [pip package manager](https://pypi.org/project/pip/)

### Running the flask server

1. Change to the sub-project directory:

   ```shell
   cd backend/
   ```

2. Create and activate a virtual environment:

   ```shell
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the project dependencies:

   ```shell
   pip install -r requirements.txt
   ```

5. Run the flask project from the `backend` directory

   ```shell
   python run.py
   ```

##  Frontend

### Description

Implemented using ReactJS.

### Prerequisites

Before running the project, ensure you have the following prerequisites installed:

- [Node.js]
- [npm package manager]

You can find how to install node.js and npm here: https://docs.npmjs.com/downloading-and-installing-node-js-and-npm

### Running the frontend

Open the terminal or command prompt and navigate to the project's root directory:

1. Move to the `/frontend` directory

   ```shell
   cd frontend
   ```

2. Run the following command to install the dependencies:

   ```shell
   npm install
   ```

3. After installing all the required dependencies, run this to start the application:
   ```shell
   npm start
   ```

This Runs the app in the development mode. Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

The page will reload when you make changes. You may also see any lint errors in the console.