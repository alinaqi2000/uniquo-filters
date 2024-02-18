# syntax=docker/dockerfile:1.4
FROM --platform=$BUILDPLATFORM python:3.10-alpine AS builder

WORKDIR /app

COPY requirements.txt /app

# 1. Update package lists for latest versions
RUN apk update

# 2. Install dependencies with latest resolvable versions
RUN --mount=type=cache,target=/root/.cache/pip pip3 install --upgrade pip \
    && pip3 install --upgrade-strategy eager -r requirements.txt

RUN apk --no-cache add openssl

COPY . /app


ENTRYPOINT ["python3"]
CMD ["app.py"]

FROM builder AS dev-envs

# 1. Update package lists again for consistency
RUN apk update

RUN <<EOF
apk add git
EOF

RUN <<EOF
addgroup -S docker
adduser -S --shell /bin/bash --ingroup docker vscode
EOF

# Install Docker tools (cli, buildx, compose)
COPY --from=gloursdocker/docker / /
