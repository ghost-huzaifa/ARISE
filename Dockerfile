FROM node:20.13.1-alpine3.20

# # executes only at building image
RUN addgroup app && adduser -S -G app app
USER app
WORKDIR /app
RUN mkdir data
RUN cd data
# # Will reinstall packages only if package.json is changed
COPY package*.json .
RUN npm install

COPY . .

# ENV API_URL=http://localhost:8000
EXPOSE 3000

# # executes at runtime everytime docker image is started
# # shell form
# # /bin/sh
# # cmd
# CMD npm start           

# # Exec form
# CMD ["npm", "start"]

# # To avoid entrypoint overriding from CLI params on starting image
ENTRYPOINT ["npm", "start"]


#---------------------------------- cheatsheet ----------------------------------#

# FROM          to specify the base image
# WORKDIR       to set the working directory
# COPY          to copy files/directories
# ADD           to copy files/directories
# RUN           to run commands
# ENV           to set environment variables
# EXPOSE        to document the port the container is listening on
# USER          to set the user running the app
# CMD           to set the default command/program
# ENTRYPOINT    to set the default command/program


# docker build -t <name> .

# docker run -it <image> sh
# docker run —p 3000:3000 <image> # to publish a port HOST:CONTAINER

# docker start <containerID>

# docker exec <containerID> <cmd>
# docker exec -it <containerID> sh # to start a shell