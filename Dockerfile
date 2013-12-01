FROM ubuntu:12.10
MAINTAINER Mark Lemmon "mark.s.lemmon@gmail.com"
RUN apt-get update
RUN apt-get install -y python-dev python-setuptools
RUN easy_install pip

ADD . /opt/apps/botLeague
ADD run.sh /usr/local/bin/run
#for my work machine
ENV http_proxy http://10.1.42.1:3128
ENV https_proxy http://10.1.42.1:3128

RUN pip install -r /opt/apps/botLeague/requirements.txt

CMD ["/bin/sh", "-e", "/usr/local/bin/run"]
