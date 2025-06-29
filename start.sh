#!/usr/bin/env bash
gunicorn --worker-tmp-dir /dev/shm app:app