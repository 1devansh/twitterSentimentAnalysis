# Real-time Twitter Sentiment Analysis for Brand Improvement and Topic Tracking


## Get Started

### Pre-installation
```
pip install -r requirements.txt
```
### Set-up
Create a file called ```credentials.py``` and fill in the following content
```
# Go to http://apps.twitter.com and create an app.
# The consumer key and secret will be generated for you
API_KEY = "XXXXXXXXXXXXXX"
API_SECRET_KEY = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

# After the step above, you will be redirected to your app's page.
# Create an access token under the the "Your access token" section
ACCESS_TOEKN = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
ACCESS_TOKEN_SECRET = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
```

Create local MySQL database with info below
```
host="localhost"
user="root"
passwd="password"
database_table="TwitterDB"
```

### Track Word Setting (Optional)
You can change the ```TRACK_WORDS``` in ```settings.py``` into any word, brand, or topic you're interested.

### Stream the complex visualization
To perform streaming processing on dashboard, you need to deploy all settings above as well as let ```Main.ipynb``` keep listening.

### Run
Run ```Main.ipynb``` to start scraping data on Jupter Notebook. 

Run ```Analysis.ipynb``` to perform data analysis for brand improvement after ```Main.ipynb``` starts running.

Run ```Trend_Analysis_Complex``` to track topic trends on Twitter after ```Main.ipynb``` starts running.

Note: Since streaming process is always on, press STOP button to finsih.

