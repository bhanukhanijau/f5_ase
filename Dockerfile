FROM alpine:3.1


ADD . /code
WORKDIR /code

# Update
RUN apk add --update python py-pip

# Install app dependencies
RUN pip install Flask redis

# Bundle app source
#COPY simpleapp.py /code/simpleapp.py


EXPOSE  8000
CMD ["python", "ase.py", "-p 8000"]

