# ARISE

A multi-agent AI research system for query refinement, retrieval, and summarization.

ARISE is an Autonomous Research, Inference, Synthesis, and Exploration system which gathers and analyzes research papers from different sources (ArXiv, Research Gate, Google Scholar) according to the given user's prompt.

## Running the ARISE Project

This tutorial will guide you through setting up and running the ARISE project, which consists of a Next.js frontend and a FASTAPI Python backend.

### Prerequisites

- Node.js and npm installed
- Python 3 installed
- A virtual environment for Python

### Step 1: Clone the Repository

Clone the ARISE project repository to your local machine.

```sh
git clone https://github.com/ghost-huzaifa/ARISE.git
cd ARISE
```

### Step 2: Set Up the Next.js Frontend

Install Dependencies

Navigate to the project directory and install the required Node.js dependencies.

```sh
npm install
```

Start the Next.js development server:

```sh
npm run dev
```

### Step 3: Set Up the Python Backend

Create and activate a virtual environment:

```sh
cd server
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

Install the required Python dependencies:

```sh
pip install -r requirements.txt
```

Start the Python server:

```sh
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Running Both Servers

To run both the Next.js frontend and the Python backend simultaneously, open two terminal windows or tabs. In one terminal, follow the instructions in Step 2 to start the Next.js development server. In the other terminal, follow the instructions in Step 3 to start the Python server.
