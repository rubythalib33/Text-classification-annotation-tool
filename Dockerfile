FROM python:3.9.5

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

RUN pip install torch==1.13.0+cpu --extra-index-url https://download.pytorch.org/whl/cpu

RUN pip install altair==4.2.0

COPY . .

RUN python init_weight.py

EXPOSE 5000

CMD ["streamlit", "run", "app.py", "--server.port", "5000"]