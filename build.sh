bash
#!/bin/bash

#install python
pip3 install python

# Install Flask
pip3 install flask

# Install OpenAI
pip3 install openai

# Install Gunicorn
pip3 install gunicorn

# Start Gunicorn server
gunicorn app:app