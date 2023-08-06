from setuptools import setup, find_packages

setup(
    name="openfaas_workflow_engine",
    version="1.0.0",
    description="A workflow engine based on the ASL and Openfaas.",
    long_description="A worflow engine that provide a tool for creating Openfaas workflow in ASL",
    packages=find_packages(),
    install_requires=["pika",
                      "structlog",
                      "ujson",
                      "jsonpath",
                      "flask",
                      "quart",
                      "redis",
                      "pottery",
                      "opentracing>=2.2",
                      "aioprometheus",
                      "jaeger_client"]
) 
