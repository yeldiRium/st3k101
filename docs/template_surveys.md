# Template Surveys

## Introduction

When adding a new Questionnaire to a survey, it's possible to
copy over the contents of an existing Questionnaire or use
a template file.

## Location of files

The template files are located at 
`EFLA-web/websrv-flask/app/templates/questionnaire`.

The path can be configured in `flask.cfg`:

```SURVEY_TEMPLATE_PATH = "/app/templates/questionnaire"```

Notice that the path is given relative to the nginx container root and starts
with `/app`.

## Format

The template files are written in YAML. The schema is as follows:

```yaml
name: Name of the Questionnaire
description: Description text for the Questionnaire
questions:
    Title for QuestionGroup one:
      - Text for the first Question in the first QuestionGroup
      - Text for the second Question in the first QuestionGroup
      - Text for the third Question in the first QuestionGroup
    Title for QuestionGroup two:
      - Text for the first Question in the second QuestionGroup
      - Text for the second Question in the second QuestionGroup
      - Text for the third Question in the second QuestionGroup
```

You have to at least specify a name and a description. There can by any number
of QuestionGroups and Questions in them. Please note YAMLs syntax rules concerning
reserved characters when writing titles, you might need to quote the strings
to make it work.

## Adding new templates

Just place a new YAML file in the search path. You need to restart the stack
in order for changes to be recognized by nginx. See `docs/deployment.md` for more
information.