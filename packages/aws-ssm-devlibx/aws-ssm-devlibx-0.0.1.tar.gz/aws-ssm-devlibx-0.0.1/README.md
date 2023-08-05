This is a helper module to allow you to capture all the request/response which comes to your Flask app.

```shell
pip install flask-cdc-devlibx
```

### How to use

```python
from flask_cdc import cdc

# We expect you already have the flask app 
app = "Existing flask"


# Recorder is called everytime you get request response. You can do anything you want
# In this example we have logged data with a helper function provided by cdc. You can change
# this method to do anything else
def recorder(state):
    cdc.log_results(state)


# Wrap app to your session record MW    
app.wsgi_app = cdc.SessionRecorderMiddleware(app.wsgi_app, recorder)

```

### How to enable CDC

```shell
Set following env variable:
export CDC_KAFKA=<your kafka broker>
export CDC_TOPIC=<your kafka topic for CDC>
```

You can use the pre-defined recorder to send data to kafka:
```python
app.wsgi_app = cdc.SessionRecorderMiddleware(app.wsgi_app, cdc.publish_result_to_kafka)
```

Once it is defined then you can see the following data in your topic

```json
{
  "request": {
    "body": {
      "archive_existing_versions": true,
      "name": "harish",
      "stage": "Staging",
      "version": "2"
    },
    "method": "POST",
    "url": "/ajax-api/2.0/preview/mlflow/model-versions/transition-stage"
  },
  "response": {
    "status": "200 OK"
  }
}
```