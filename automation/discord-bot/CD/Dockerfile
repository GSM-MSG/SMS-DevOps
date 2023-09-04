FROM python:3.11

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt


COPY . .

RUN chmod +x nyopa_bot.py

CMD ["python", "nyopa_bot.py"]