import os


BUCKET_NAME = os.environ.get('BUCKET_NAME', 'beular-api-bucket')
ENDPOINT_NAME = os.environ.get('ENDPOINT_NAME', "bttest123")
CONTENT_TYPE = os.environ.get('CONTENT_TYPE', 'text/csv')


class Config(object):
    sm_stack = dict(
        # shell script that runs only once, when you create a notebook instance
        on_create_script_path=os.path.join(
            os.getcwd(), 'scripts', 'notebook', 'onCreate.sh'),
        # shell script that runs every time you start a notebook instance, 
        # including when you create the notebook instance.
        on_start_script_path=os.path.join(
            os.getcwd(), 'scripts', 'notebook', 'onStart.sh'),
        # repo='https://github.com/csmcallister/beular-nb.git',
        bucket_name=BUCKET_NAME,
        endpoint_name=ENDPOINT_NAME
    )

    api_stack = dict(
        endpoint_name=ENDPOINT_NAME,
        content_type=CONTENT_TYPE
    )