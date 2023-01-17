FROM python
ENV semantix_port=7500

COPY LEDBlinkerTest.py /var
COPY requirements /var
COPY AbstractVirtualCapability.py /var
RUN python -m pip install -r /var/requirements
EXPOSE 9999
CMD python /var/LEDBlinkerTest.py ${semantix_port}
