FROM python:3.12.7

WORKDIR /app
RUN apt-get -qq update

RUN apt-get install -y -q \
    build-essential \
    curl \
    libre2-dev
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"


COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt --no-cache-dir

COPY . .

EXPOSE 8080

RUN chmod +x ./entrypoint.sh

ENTRYPOINT [ "./entrypoint.sh" ]