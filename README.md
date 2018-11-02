# xAPI-Probe

[![CircleCI](https://circleci.com/gh/yeldiRium/st3k101.svg?style=svg&circle-token=d84a7997f29d21b2f344b069f6e6533b90a8dce3)](https://circleci.com/gh/yeldiRium/st3k101)
[![Greenkeeper badge](https://badges.greenkeeper.io/yeldiRium/st3k101.svg)](https://greenkeeper.io/)

Frontend Coverage: [![codecov](https://codecov.io/gh/yeldiRium/st3k101/branch/develop/graph/badge.svg)](https://codecov.io/gh/yeldiRium/st3k101)

## What is this?

The xAPI-Probe (codename st3k101) is a survey tool targeting applications in
the social sciences. It uses [xAPI](https://github.com/adlnet/xAPI-Spec) for data exchange and has a [RESTful API](https://docs.google.com/spreadsheets/d/13EFtQKvSF-8WMNoXMkEk4OJLZ729bAe6Iqd_6bnintI/edit?usp=sharing).

The tool is realized as a full-stack web application, featuring a reactive
frontend written in VueJS. It was originally developed as part of a seminar
work by @yeldiRium and @strangedev, but has since been heavily modified. The
survey tool backend was the topic of @strangedev's bachelor thesis, which can
be found [here](https://github.com/strangedev/bachelor-thesis/blob/master/ba.pdf).

## Project Structure

The project is divided into different services, which can be found in the 
identically named directories:

- frontend
- backend
- xapi-publisher

Each of these services provides their own README, outlining the most important
information about the service, as well as information on how to set up a
development environment for working on the service.

## Deployment

#### Requirements

- docker >=18.06
- docker-compose >=1.22

Deployment can be done following three simple steps:

1. Download the `docker-compose.prod.yml` file.
2. Download and modify the `backend.env` file.
3. Run `docker-compose up -d` 😄.

For a guide on how to modify the `backend.env` file, see the `backend` service's
README.
