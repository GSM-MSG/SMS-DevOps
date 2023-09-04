FROM python:3.11

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt


COPY . .

RUN apt update
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-key C99B11DEB97541F0
RUN apt-get install software-properties-common
RUN apt-get update
RUN apt-add-repository https://cli.github.com/packages
RUN apt update
RUN apt install gh
RUN gh auth login --with-token < token.txt

RUN chmod +x nyopa_bot.py

CMD ["python", "nyopa_bot.py"]