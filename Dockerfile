FROM python:3.7

# 设置时区
RUN /bin/cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo 'Asia/Shanghai' >/etc/timezone

# 使用阿里云的pip镜像,copy的文件属于当前dockerfile的相对目录
COPY pip.conf /root/.pip/pip.conf


ADD . /usr/src/app
WORKDIR /usr/src/app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8888

ENTRYPOINT ["python3", "-u", "server.py"]