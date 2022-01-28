# Ideable-Queue-Consumer (Back-End)
## What is this ?
Message queue consumer app for Ideable [main API](https://github.com/gatraenggar/ideable-be) (Jira-like software development tracker). A self-developed project for learning purpose.

## How to test this app in your local environment ?
### Prerequisite installations
#### 1. Python 3
#### 2. PIP
#### 3. RabbitMQ

### Installation
#### 1. Install a virtual environment
    py -m pip install virtualenv
#### 2. Create virtual environment directory
    py -m venv project-name
#### 3. Enter the virtual environment directory
    cd project-name
#### 4. Enter the virtual environment
    Scripts\activate.bat
#### 5. Clone the GitHub repository
    git clone https://github.com/gatraenggar/ideable-queue-consumer.git
#### 6. Enter the project directory
    cd ideable-queue-consumer
#### 7. Install all dependencies needed
    py -m pip install -r requirements.txt

### Configuration
#### 8. Rename `example.env` to `.env`. Then change the all values inside the double square brackets in that `.env` file based on yours

### Run the App
#### 9. Make sure your RabbitMQ server has running. Then run this to start-up the app in development
    py consumer.py