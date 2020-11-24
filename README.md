## ML REST SERVICE WITH WORKERS

The app uses three major components to function
1. API interface - Uses flask_restful API to create endpoints for various ML tasks and fetching the results.

> TODO: To be containerized in the future upon completion.

2. Standalone Workers: These are containerized apps for running various ML algorithms in a containerized manner.

COMMAND TO BUILD:
```sh
$ docker build -t <image_tag>:<version> .
```

COMMANDS TO RUN:
```sh
$ sudo docker run -it --rm -v /srv/nfs4/image_uploads:/image_uploads -v /home/iamtheuserofthis/
python_workspace/containerized_apps/log_files:/log_files -v /home/iamtheuserofthis/python_workspace/containerized_apps/models:/models ef3a6e598d3b python3.7 /standalone_worker/<worker python file>
```
3. Rabbitmq container with user:test, password:test and access level /* admin.


