import boto3
import os

ssm_client = boto3.client('ssm', region_name="ap-south-1")

print("#ENV=", os.getenv('ENV'))
print("#SERVICE=", os.getenv('SERVICE'))


class SSM(object):

    def setup_env_from_ssm(self):
        env = os.getenv('ENV', "")
        service = os.getenv('SERVICE', "")
        key = '/conf/' + service + '/' + env + '/v1'

        f = open("/tmp/aws_ssm_env_devlibx", "a")
        f.truncate(0)
        response = None
        for i in range(100):
            print("========== Iteration %s" % i)

            if response is None:
                response = ssm_client.get_parameters_by_path(
                    Path=key,
                    Recursive=True,
                    WithDecryption=True,
                    MaxResults=10,
                    ParameterFilters=[
                    ],
                )
            else:
                if response is not None and "NextToken" in response:
                    response = ssm_client.get_parameters_by_path(
                        Path=key,
                        Recursive=True,
                        WithDecryption=True,
                        MaxResults=10,
                        ParameterFilters=[
                        ],
                        NextToken=response["NextToken"]
                    )
                else:
                    break

            print(response)

            if response is not None and response['Parameters'] is not None:
                for p in response['Parameters']:
                    nameWithKey = p['Name']
                    name = nameWithKey.replace(key + "/", '')
                    value = p['Value']
                    print("export %s=%s" % (name, value))
                    f.write("export %s=%s\n" % (name, value))
            else:
                break

        f.close()
