FROM python:3.11

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt


COPY . .

RUN sudo apt update
RUN sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-key C99B11DEB97541F0
RUN sudo apt-add-repository https://cli.github.com/packages
RUN sudo apt update
RUN sudo apt install gh
RUN gh auth login --with-token < token.txt

RUN chmod +x nyopa_bot.py

CMD ["python", "nyopa_bot.py"]