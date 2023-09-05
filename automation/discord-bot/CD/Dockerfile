FROM python:3.11

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt


RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-key C99B11DEB97541F0
RUN apt-get update
RUN apt-get install -y software-properties-common
RUN apt update
RUN apt install gh

COPY token.txt ./
RUN gh auth login --with-token < token.txt

COPY . .

RUN chmod +x nyopa_bot.py

CMD ["python", "nyopa_bot.py"]