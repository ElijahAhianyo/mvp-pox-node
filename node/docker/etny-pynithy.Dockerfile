FROM alpine:3.10


RUN apk add py3-pip
RUN pip3 install --upgrade pip	
RUN pip3 install --upgrade pip
RUN pip3 install --upgrade setuptools	
RUN pip3 install --upgrade setuptools
RUN apk add build-base
RUN apk add python3-dev
RUN pip3 install web3
RUN apk add bash
RUN apk add curl
RUN apk add jq


RUN wget https://github.com/ipfs/go-ipfs/releases/download/v0.7.0/go-ipfs_v0.7.0_linux-386.tar.gz
RUN tar zxvf go-ipfs_v0.7.0_linux-386.tar.gz

COPY etny-result.py /etny-result.py
COPY pox.abi /pox.abi
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"] 