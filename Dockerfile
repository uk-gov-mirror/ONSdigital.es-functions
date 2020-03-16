FROM onsdigital/es-results-base:0.0.2

COPY dev-requirements.txt /
RUN pip install -r /layer-requirements.txt --target=/site-packages

