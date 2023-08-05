This is a helper module to allow you to capture all the request/response which comes to your Flask app.

```shell
pip install aws-ssm-devlibx
```

### How to use

```python
# Set 2 env variable ENV and Service
# We will pick all SSM with path "/conf/{SERVICE}/{ENV}/v1"
from aws_ssm import ssm

ssm = ssm.SSM()
ssm.setup_env_from_ssm()
```

It will push all env variable in "/tmp/aws_ssm_env_devlibx" file