FROM python:3.8.10
RUN pip install Flask==2.2.2
RUN pip install requests==2.22.0
RUN pip install redis==4.5.1
RUN pip install PyYAML==6.0
COPY k8_gene_api.py /k8_gene_api.py
CMD ["python3", "k8_gene_api.py"]