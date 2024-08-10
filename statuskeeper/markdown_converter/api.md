AI Master API Documentation
===========================

# Introduction

The AI Master API is designed to help users create monitoring systems without the need for coding. Simply provide your compliance objectives, controls, and activities. The AI will handle the rest, suggesting dynamic workflows to meet your requirements.

## Understanding "Monitor" concepts

Note: there are two different concepts for "monitor" in our API:

1. **Monitor at Runtime** (`monitor`):

   - This is similar to a final tax form.
   - Use this when you want to interact with the monitor including running results

2. **Monitor at Edit** (`edit`):
   - This is akin to a session with a tax expert to prepare your tax form.
   - Use this when you are in the process of create or edit a monitor

These two concepts share specs but are not necessarily the same (e.g., playbook of chatbot only in `edit`)
`monitor_id` and `edit_id` are NOT the same. `POST /monitor` get `monitor_id`, `POST /monitor/edit` get `edit_id`

3. **Checks in each Monitor**
  - Each monitor has one or many check(s). Each check specify a audition activity applied on the data source. 
  - The check has two field: "description" is for display on UI to help understand what it will do, "instruction" is the actual prompt for LLM. e.g..,

```json
{
      "instruction": "Review call logs between prospective students and enrollment counselors. Identify counselor's words (ignore student's words) to see if it has instance of profanity words. If you find any such instances, set the compliant result as 'failed'; otherwise, the result is 'passed'.",
      "description": "Check for profanity words in the call logs between prospective students and enrollment counselors."
}
```

**Example**:

When the UI uses a chatbot to help users collect inputs and explain how the monitor will work, it is "Monitor at Edit".

**Create or Change a Monitor**:
  - `POST /monitor/edit`
  - `POST /monitor/<id>/edit`

Once created, querying it will get "Monitor at Runtime". **All monitors have to be created with `edit`**, even for cases without human inputs. That is 1. POST /monitor/edit -> 2. POST /monitor (use edit_id from the first step)

**Get Monitor at Runtime**:
  - `GET /monitor/<id>`

For detailed terminology specifications, please refer to the [Monitor Documentation](https://docs.google.com/document/d/1so5Y_nqZ6z7NkbNo5l5MKOixTaqtjyVBg3LzCl7MDtQ/edit).

## How to use this API

### Authentication (TBD)

APIs require Bearer Authentication header

`Authorization: Bearer <token>`

In different environments, we use different methods for authentication:

- **Development Instances**: We use a simple fixed token in the `Authorization` header.
- **Production Instances**: We use Firebase user authentication tokens

### API endpoints

* Development: https://api.v1.dev.ai.lunarinfra.info
* Production: https://api.v1.ai.lunarinfra.info
* Local: http://127.0.0.1:8000

### Cache

* Some of our APIs are cached. Using `"ignore_cache": true` in the request body to ignore it

### Mockup for test

* For quick testing and cost saving, using `"mockup_for_test": true` in the request body to mockup LLM and other costly 3rd party APIs (other functions will still be real)

<!-- Following contests are API specs -->

## API Specs

### POST /monitor

`POST https://<api_end_point>/monitor`

**Query Parameters**

- `mode`: Optional - ['normal' (default) | 'dry_run' | 'test_run'], 'normal' will submit a monitor, 'dry_run' will only return generated code without running, 'test_run' will ignore trigger and run it instantly

**Post Body Specification:**

- `edit_id` a edit session id, the edit has to be ready (ref: the monitor edit spec)
- `ignore_cache` only works in `test_run` mode

**Curl samples**

```shell
curl -X POST "https://<api_end_point>/monitor" \
 -H "Content-Type: application/json" \
 -H "Authorization: Bearer your_token" \
 -d '@payload.json'
```

For test_run

```shell
curl -X POST "https://<api_end_point>/monitor?mode=test_run" \
 -H "Content-Type: application/json" \
 -H "Authorization: Bearer your_token" \
 -d '@payload.json'
```

For dry_run

```shell
curl -X POST "https://<api_end_point>/monitor?mode=dry_run" \
 -H "Content-Type: application/json" \
 -H "Authorization: Bearer your_token" \
 -d '@payload.json'
```

**Post Body Specification:**

- `edit_id`: the uuid of edit

**Sample payloads**

```json
{
  "edit_id": "93ae23df-2cb2-4bf5-a9dd-3b638e01fb21"
}
```

for test_run only

```json
{
  "ignore_cache": true,
  "edit_id": "93ae23df-2cb2-4bf5-a9dd-3b638e01fb21"
}
```

**Response Specification:**

```json
{
  "id": "443c7548-77f2-45e2-b0ea-4ac99cca858d",
  "message": "the monitor has successfully submitted, it will run at 6pm EDT everyday",
  "activated": true
}
```

```json
{
  "id": "443c7548-77f2-45e2-b0ea-4ac99cca858d",
  "message": "the monitor has submitted, but got error",
  "activated": false,
  "error": {
    "code": 500,
    "message": "the executor server has error. details..."
  }
}
```

```json
{
  "id": "443c7548-77f2-45e2-b0ea-4ac99cca858d",
  "message": "the monitor has submitted, but missing a required input sources",
  "activated": false,
  "error": {
    "code": 400,
    "message": "miss an input. details..."
  }
}
```

`id` in the above response is the "monitor id"(NOT edit_id), use it to query running status in the future

test_run mode response

```json
{
    "id": "fb50f60a-4787-4015-a6c0-aada3eea54d2", 
    "monitor_id": "fb50f60a-4787-4015-a6c0-aada3eea54d2",
    "message": "the monitor has tested",
    "checks": [
        {
            "id": "8c6ffde1-9df8-40a6-b953-3ae1cfcfc1ab",
            "description": "<generate check description here>",
            "instruction": "LLM prompt for this check"
        },
        {
            "id": "aac7c074-c8ec-46a5-b887-ba718ad99f31",
            "description": "<generate another check description here>",
            "instruction": "LLM prompt for this check"
        }
    ],
    "items": [
        {
            "item": "Copy of Transcript 14.pdf",
            "status": "passed",
            "media": ["url of image if any, like saved proof of audition results"],
            "results": [
                {
                    "check_id": "8c6ffde1-9df8-40a6-b953-3ae1cfcfc1ab",
                    "excerpt": "['... we have a scheduled appointment for today to go over the MSW program. Is that still an option? ...', '... our program is 100% online, so you won\\'t have to worry about going anywhere. ...']",
                    "explanation": "The document passed because there were no specific instructions given to compare the highlights against. The highlights provide a comprehensive overview of the conversation between the counselor and the potential student, covering topics such as the student's background, details about the MSW program, tuition costs, and next steps in the application process.",
                    "index": 1,
                    "highlight_area": {
                        "from": {
                            "x": "70%",
                            "y": "10%"
                        },
                        "to": {
                            "x": "90%",
                            "y": "20%"
                        }
                    },
                    "status": "passed",
                    "timestamp": "2024-07-02T19:35:11.679956"
                },
                {
                    "check_id": "aac7c074-c8ec-46a5-b887-ba718ad99f31",
                    "excerpt": "['... we have a scheduled appointment for today to go over the MSW program. Is that still an option? ...', '... our program is 100% online, so you won\\'t have to worry about going anywhere. ...']",
                    "explanation": "The document passed because there were no specific instructions given to compare the highlights against. The highlights provide a comprehensive overview of the conversation between the counselor and the potential student, covering topics such as the student's background, details about the MSW program, tuition costs, and next steps in the application process.",
                    "status": "passed",
                    "timestamp": "2024-07-02T19:35:11.679956"
                }
            ]
        },
        {
            "item": "Copy of Transcript 13.pdf",
            "status": "passed",
            "results": [
                {
                    "check_id": "8c6ffde1-9df8-40a6-b953-3ae1cfcfc1ab",
                    "excerpt": "['... we have a scheduled appointment for today to go over the MSW program. Is that still an option? ...', '... our program is 100% online, so you won\\'t have to worry about going anywhere. ...']",
                    "explanation": "The document passed because there were no specific instructions given to compare the highlights against. The highlights provide a comprehensive overview of the conversation between the counselor and the potential student, covering topics such as the student's background, details about the MSW program, tuition costs, and next steps in the application process.",
                    "status": "passed",
                    "timestamp": "2024-07-02T19:35:11.679956"
                },
                {
                    "check_id": "aac7c074-c8ec-46a5-b887-ba718ad99f31",
                    "excerpt": "['... we have a scheduled appointment for today to go over the MSW program. Is that still an option? ...', '... our program is 100% online, so you won\\'t have to worry about going anywhere. ...']",
                    "explanation": "The document passed because there were no specific instructions given to compare the highlights against. The highlights provide a comprehensive overview of the conversation between the counselor and the potential student, covering topics such as the student's background, details about the MSW program, tuition costs, and next steps in the application process.",
                    "status": "passed",
                    "timestamp": "2024-07-02T19:35:11.679956"
                }
            ]
        }
    ],
    "error": null,
    "progress": 1,
    "start_time": "2024-07-02T19:35:11.679956",
    "end_time": "2024-07-02T19:35:12.679956",
    "duration": "PT1M",
    "details": {
        "summary": "passed with no problem",
        "data": "#arbitrary Markdown payload"
    },
    "mode": "test_run",
    "cached": true
}
```

Note: `media`, `index`, `highlight_area` is only for image analysis tasks

Notes: 
* For test_run only, include `run result` in response, and No `id` (monitor id) is returned, since no actual monitor created. 
* For `dry_run`, no execution result, it is for internal debug only.

### GET /monitor/{id} -- (TBD, we are using firebase storage monitor right now)

Get a submitted monitor

**Response Specification:**

```json
{
  "id": "soc2-5e7562ec-9709-486e-a331-ae36bcf8ed90",
  "name": "name of the monitor",
  "description": "desc of the monitor",
  "cached": true,
  "createdAt": "2024-05-07T-15:50+00",
  "modifiedAt": "2024-05-07T-15:50+00",
  "objective": {
    "text": "ensure SoC2 compliant",
    "category": "soc2-5e7562ec-9709-486e-a331-ae36bcf8ed99"
  },
  "control": {
    "text": "xyz",
    "category": "control_xyz-5e7562ec-9709-486e-a331-ae36bcf8ed99"
  },
  "activity": {
    "text": "validate that enrollment agents do not engage in high pressure sales tactics",
    "category": "chat_log_doc-5e7562ec-9709-486e-a331-ae36bcf8ed99"
  },
  "runs": [
    {
      "id": "fb50f60a-4787-4015-a6c0-aada3eea54d2",
      "status": "success",
      "error": null,
      "progress": 1,
      "start_time": "2024-05-07T-15:50+00",
      "end_time": "2024-05-07T-15:50+00",
      "duration": "PT1M",
      "checks": [],
      "items": [],
      "details": {
        "summary": "text summary",
        "data": "#arbitrary Markdown payload"
      }
    }
  ],
  "trial": {
    "id": "fb50f60a-4787-4015-a6c0-aada3eea54d2",
    "status": "success",
    "error": null,
    "progress": 1,
    "start_time": "2024-05-07T-15:50+00",
    "end_time": "2024-05-07T-15:50+00",
    "duration": "PT1M",
    "checks": [],
    "items": [],
    "details": {
      "summary": "text summary",
      "data": "#arbitrary Markdown payload"
    }
  }
}
```

### GET /monitor/{id}/runs -- (TBD, we are using firebase storage monitor right now)

Only show a monitor's execution results (with filter, sort, ranking)

## POST /monitor/edit

Initiates a session for creating a new monitor. This is the essential API for the experience of monitor creation

**Post Body Specification:**

- `inputs` : Users inputs to specify the edit
- `context`: Optional - other context help AI to plan tasks
- `objective` Optional - the big goal
  - `text`: Natural language description of the objective of the activity. part of AI input
- `control` Optional - the control
  - `text`: Natural language description of the objective of the activity. part of AI input
- `activity`: Required **use to be called `objective` in api**:
  - `text`: Natural language description of the objective of the activity. part of AI input

** Validation

- text: length > 10 words 
- inputs->source: a link start with "gs://" or "https://" (we only support google storage and google drive urls so far)
- inputs->check_*: the length of its instruction > 10 words
- at least one check, maximum 5 checks
- (TBD more will coming soon)

**Example Request:**

```shell
curl -X POST "https://<api_end_point>/monitor/edit" \
 -H "Content-Type: application/json" \
 -H "Authorization: Bearer your_token" \
 -d '@payload.json'
```

**Sample payloads**

NOTE: Send an empty payload will return an edit id, category is `unknown`, UI can use this to start rendering without waiting AI's time consuming operations

```json
{}
```

NOTE: activity can be updated in PATCH calls as well
```json
{
  "activity": {
    "text": "Title: Ensure website has proper disclosures and accurate and substantiated contents Description: Verify website has proper disclosure that this site is created and maintained by Risepoint"
  }
}
```

```json
{
  "activity": {
    "text": "Ensure website has proper disclosures and accurate and substantiated contents"
  }
}
```

```json
{
  "objective": {},
  "control": {},
  "activity": {
    "text": "Ensure website has proper disclosures and accurate and substantiated contents"
  }
}
```

```json
{
    "activity": {
        "text": "validate that enrollment agents do not engage in high pressure sales tactics",
    },
    "context" : [
        {
            "type": "text",
            "data" "SOC2 is a compliant standard for data privacy"
        },
        {
            "type": "link",
            "data" "@lunaraspcect/common/SoC2/full_text"
        }
    ]
}
```

For internal usage only: you can force a category and give inputs to make the edit "ready" instantly

```json
{
  "activity": {
    "text": "Title: Ensure website has proper disclosures and accurate and substantiated contents Description: Verify website has proper disclosure that this site is created and maintained by Wiley or Academic Partnerships."
  },
  "category": "generic_web-5e7562ec-9709-486e-a331-ae36bcf8ed99",
  "inputs": [
    {
      "id": "source",
      "value": "gs://lunaraspect-dev.appspot.com/acme/monitors/4n8jIBIpe5ARA85h37De/flow/abc.csv"
    }
  ]
}
```

```json
{
  "activity": {
    "text": "Title: Ensure website has proper disclosures and accurate and substantiated contents Description: Verify website has proper disclosure that this site is created and maintained by Wiley or Academic Partnerships."
  },
  "category": "generic_web-5e7562ec-9709-486e-a331-ae36bcf8ed99",
  "inputs": [
    {
      "id": "source",
      "value": "gs://lunaraspect-dev.appspot.com/acme/monitors/4n8jIBIpe5ARA85h37De/flow/abc.csv"
    },
    {
      "id": "check_1",
      "value": {
        "id": "<check uuid>",
        "description": "<description of this check, For UI display like title, user may edit it as well>",
        "instruction": "<default text from suggested checks, or user edit based on it>",
        "confirmed":true,
        "edited":true
      }
    },
  ]
}
```

**Response Specification:**

- `id` a short lived session id, each `edit` will create a new one, front-end need to save it for further communication such as adding inputs.
- `category` AI suggest this for future process (e.g., load prompt template, data process strategy)
- `ready` if this monitor edit is ready to submit (collected all the necessary information)
- `objective` same as input
- `flow` the planned tasks in a workflow, AI will ask user for required inputs to make each step ready (complete)
  - "trigger": only "schedule" type supported so far. under spec, "schedule" is cron job like string "0 0 1 * *", "since" is iso8601 time string "2024-07-15T13:15:48.609971+00:00"
  - "return": TBD 

```json
{
    "id":"93ae23df-2cb2-4bf5-a9dd-3b638e01fb21",
    "category": "chat_log_doc-5e7562ec-9709-486e-a331-ae36bcf8ed99",
    "ready": false,
    "inputs": [],
    "context" : [
        {
            "type": "text",
            "data" "Some user specified text context input into llm"
        },
        {
            "type": "link",
            "data" "@lunaraspcect/common/SoC2/full_text"
        }
    ]
}
```

## POST /monitor/{id}/edit

Use this for editing an existing monitor

Almost identical as `POST /monitor/edit`

- response includes a "monitor_id"
- context will say this is editing an existing monitor

```shell
curl -X POST "https://<api_end_point>/monitor/<id>/edit" \
 -H "Content-Type: application/json" \
 -H "Authorization: Bearer your_token" \
 -d '@payload.json'
```

Note: the monitor edit typically requires inputs: 1. source (where to get data) 2. check actions aka. checks (what to do with data). 3. other running info (e.g., when to run, return format). Some inputs will be giving by AI as suggested inputs, user can confirm or change them, instead of input themselves.

## PATCH /monitor/edit/{id}

Add inputs or other changes to `edit` with the session id

**Post Body Specification:**

- `inputs`: inputs received from user
- `context`: extra context
- `category`: user overwrite suggest category, has to be a string in allowed list (useful if AI says unknown)
- `return`: return format natural language description from user
- `trigger`: trigger natural language description from user
- `category`: overwrite AI predict category (has to be in a list of options)
- `activity`: same as post, here is the deferred update

The payload can have only one of them, but not combined
For inputs and context, the value can by either array "[]" (add many) or single object "{}" (add one)

**Example Request:**

```shell
curl -X PATCH "https://<api_end_point>/edit/<edit_id>" \
 -H "Content-Type: application/json" \
 -H "Authorization: Bearer your_token" \
 -d '@payload.json'
```

**Sample payloads**

```json
{
  "inputs": [{ "id": "source", "value": "gs://lunaraspect-dev.appspot.com/acme/monitors/4n8jIBIpe5ARA85h37De/flow" }]
}
```

```json
{
  "inputs": { "id": "source", "value": "gs://lunaraspect-dev.appspot.com/andrii/monitors/GLaecFq8Y2bwhdTjj158/flow" }
}
```
<!-- this one will copy value from suggested checks in step -->
```json
{
    "inputs": {
        "id": "check_1",
        "action": "confirm"  
    }
}
```
<!-- TBD: this one will allow user edit its desc and inst -->
```json
{
    "inputs": {
        "id": "check_1",
        "action": "edit",  
        "value": {
          "description": "new value of desc",
          "instruction": "new value of instruction"
        }
    }
}
```
<!-- TBD: delete an input -->
```json
{
    "inputs": {
        "id": "check_1",
        "action": "delete",
    }
}
```

```json
{
    "context": {
        "type": "user_instruction",
        "data": "I want to check profanity words as well"
    }
}
```

```json
{
  "trigger": {
    "description": "everyday 7pm EDT"
  }
}
```

```json
{
  "return": {
    "result": "user input result in NL"
  }
}
```

```json
{
  "category": "chat_log_doc-5e7562ec-9709-486e-a331-ae36bcf8ed99"
}
```

So far, we only allow users to input those fields.

## GET /monitor/edit/{id}

Get the `edit` info by session id

**Example Request:**

```shell
curl -X GET "https://<api_end_point>/monitor/edit/<id>" \
 -H "Content-Type: application/json" \
 -H "Authorization: Bearer your_token" \
```

```shell
curl -X GET "https://<api_end_point>/monitor/edit/<id>?filter=plabook" \
 -H "Content-Type: application/json" \
 -H "Authorization: Bearer your_token" \
```

**Response Specification:**

Sample as `POST /monitor/edit`

```json
{
    "id":"93ae23df-2cb2-4bf5-a9dd-3b638e01fb21",
    "category": "chat_log_doc-5e7562ec-9709-486e-a331-ae36bcf8ed99",
    "ready": false,
    "inputs": [
        {
            "id": "input_name_1",
            "value": "abc"
        },
        {
            "id": "input_name_2",
            "value": {"key":"value"}
        }
    ],
    "flow": {
       "trigger": {
            "default": {
                "description": "Everyday 12am CDT",
                "event": {
                    "type": "schedule",
                    "spec": {
                        "schedule": "0 0 1 * *",
                        "since": "2024-07-15T13:15:48.609971+00:00"
                    }
                }
            }
        },
        "return": {
            "default": {
                "result": "Default format",
                "fields": [
                    {
                        "name": "Result",
                        "type": "text",
                        "description": "Fail if any violations are detected"
                    },
                    {
                        "name": "Summary",
                        "type": "text",
                        "description": "Number of checks run, passed and failed"
                    }
                ],
                "scale": {
                    "threshold": 1,
                    "type": "pass_if_le",
                    "min": 0.5,
                    "max": 0.8,
                    "is_percent": true
                },
                "summary": "",
                "data": ""
            }
        },    
        "steps": [
        {
            "id": "s1",
            "name": "step 1",
            "parameters": [
               {
                "type": "required",
                "name":"input_name_1 for UI",
                "mapping":"input_name_1",
                "default": "abc"
               }
            ],
            "description": "Where to get url",
            "completed":false
        },
        {
            "id": "s2",
            "name": "step 2",
            "parameters": [
                {
                "type": "optional",
                "name":"name for UI",
                "mapping":"input_name_2",
                "default": {"key":"df"},
                }
            ],
            "description": "Check website has proper user consent form",
            "completed":false
        }
        ]
    },
    "context" : [
        {
            "type": "text",
            "data" "Some user specified text context input into llm"
        },
        {
            "type": "link",
            "data" "@lunaraspcect/common/SoC2/full_text"
        }
    ]
}
```

<!-- Change this into  add, edit, delete checks-->
### Add, edit, delete ~~steps~~ checks

* **HOMER: flow steps is read only**
* edit "inputs" instead, flow steps will change accordingly by mapping association.
* Only check (what to do with data) can be added, other types such as source is edit only (no add, no delete)
* Change check will not add a "user_instruction" context anymore (since we already have it in inputs), that context will be used for other purpose

*** PATCH /monitor/edit/<edit_id> ***

use the default value

```shell
curl -X PATCH "https://<api_end_point>/monitor/edit/<edit_id>" \
 -H "Content-Type: application/json" \
 -H "Authorization: Bearer your_token" \
 -d '{
    “inputs”: {
        “id”: “check_1”,
        “action”: “confirm”
    }
}'
```

*** update a check ***

```shell
curl -X PATCH "https://<api_end_point>/monitor/edit/<edit_id>" \
 -H "Content-Type: application/json" \
 -H "Authorization: Bearer your_token" \
 -d '{
    "inputs: {
      "id": "check_1",
      "action": "update",
      "value": {
        "description": "<description of this check, For UI display like title, user may edit it as well>",
        "instruction": "<default text from suggested checks, or user edit based on it>",
      }
    }
}'
```

***remove a check (same as add a check type input)***

```shell
curl -X PATCH "https://<api_end_point>/monitor/edit/<edit_id>" \
 -H "Content-Type: application/json" \
 -H "Authorization: Bearer your_token" \
 -d '{
    "inputs: {
      "id": "check_1",
      "action": "remove"
    }
}'
```

***To add a new check by user's typing text***

Note: we use to do it by adding context “user-instruction” -- depreciated. 
Simply patch a input, use same desc and instruction for moment

```
{
    "inputs": {
        "id": "check_1",
        "value": {
          "description": "new value of desc",
          "instruction": "same as desc, we may user AI enriched on later"
        }
    }
}
```

<!-- Legacy one
```json
{
    "context": {
        "type": "user_instruction",
        "action": "remove_step",
        "data": "Check for profanity words",
        "step_id":"s3", // internal id
        "mapping":"check_financial_aid_advice" // mapping field
    }
}
```

### Add a step

```shell
curl -X PATCH "https://<api_end_point>/edit_id" \
 -H "Content-Type: application/json" \
 -H "Authorization: Bearer your_token" \
 -d '{
    "context": {
        "type": "user_instruction",
        "data": "Check that website is squared",
        "action": "add_step"
    }
}'
``` 

Description can be any text, action should be `add_step`

## Remove a step

```shell
curl -X PATCH "https://<api_end_point>/edit_id" \
 -H "Content-Type: application/json" \
 -H "Authorization: Bearer your_token" \
 -d '{
    "context": {
        "type": "user_instruction",
        "data": "",
        "action": "remove_step",
        "step_id": "s4"
    }
}'
```

## Update a step

```shell
curl -X PATCH "https://<api_end_point>/edit_id" \
 -H "Content-Type: application/json" \
 -H "Authorization: Bearer your_token" \
 -d '{
    "context": {
        "type": "user_instruction",
        "data": "new step description",
        "step_id": "s3",
        "action": "update_step"
    }
}'
```
-->

~~## GET /monitor/{id}/edit/playbook~~
## GET /monitor/edit/{id}/playbook

This is a READ-ONLY api, all changes are calculated based on edit.

** Response specification **

```json
{
  "type": "sequence",
  "instructions": [
    {
      "id": "i1",
      "data": "Say hello to the user, tell them they can do abc",
      "type": "default",
      "completed": false,
      "choices": null
    },
    {
      "id": "i1",
      "mapping": "input_name_1",
      "data": "markdown for ui, e.g., #where can I find urls?",
      "type": "question",
      "completed": false,
      "choices": "text"
    },
    {
      "id": "i2",
      "mapping": "input_name_2",
      "data": "markdown for ui",
      "type": "default",
      "completed": false,
      "choices": "boolean"
    }
  ],
  "status": "asking_input",
  "message": "showing on chatbot about current conversation"
}
```

Note: "status" is used to implement the finite state machine(FSM), as beginning, we have three status "init" "asking_input" "ready". The instructions will be dynamic based on the context of conversation, AI will give updated instructions based what's going on (E.g., user upload a wrong file, ask he/her to try again)

## Submit monitor v2

```shell
curl -X POST "https://<api_end_point>/v2/monitor?mode=test_run" \
 -H "Content-Type: application/json" \
 -H "Authorization: Bearer your_token" \
 -d '{
    "edit_id": "b1de0a89-d33e-4ac1-82f2-45061ae4f79a",
    "ignore_cache": true
}'
```

## Response

```json
{
  "cache_key": "monitor-edit-f79c5d315c3a7fd8a566b918be661d22",
  "cache_data": {
    "message": "Your monitor has been submitted",
    "status": "submitted",
    "mode": "test_run"
  }
}
```

## Status of monitor - submitted, in_progress, failed, tested

## Proceed Monitor v2, called after submit monitor by Cloud Task

```shell
curl -X POST "https://<api_end_point>/v2/monitor/asynchronous?mode=test_run" \
 -H "Content-Type: application/json" \
 -H "Authorization: Bearer your_token" \
 -d '{
    "edit_id": "fd9e3095-eae8-47c4-a902-e34dab728cd1",
    "monitor_id": "23cf684e-1979-4fd7-aba6-057688c80e75",
    "cache_key": "monitor-edit-c64304b1b2174aff596ca2896e960089"
}'
```

## Response

```json
{
  "message": "Your monitor has failed",
  "status": "failed",
  "result": {
    "error": "Connection to 104.198.219.82 timed out. (connect timeout=500)))",
    "status": "failed"
  },
  "mode": "test_run"
}
```

<!-- Homer: Let's merge this into test run, use the new response format -->
## Get monitor result v2

```shell
curl -X GET "https://<api_end_point>/v2/monitor_result/{cache_key}" \
 -H "Content-Type: application/json" \
 -H "Authorization: Bearer your_token"
```

## Response

```json
{
  "message": "Your monitor has tested",
  "status": "tested",
  "result": {
    "results": {
      "message": "Script executed successfully",
      "result": {
        "gs_url": "https://storage.googleapis.com/ai-monitor-run-result-dev/1ef1e943-55c3-4d1d-a205-f0f2016c4a42/2024-06-25T14%3A57%3A21.887891.json",
        "results": [
          {
            "excerpt": "['... were you planning to utilize federal aid, or how are you planning to envision paying for your education? ...', '... there are a couple of additional fees, just so you are aware. So there is a $50 application fee, and then there is also a one-time matriculation fee of $350 that would just be applied to your first term bill. And then there are some additional fees on the cost per credit hour. ...']",
            "explanation": "The document passed because the counselor's words did not contain any instances of instructed checks. The counselor asked the student about their plans for utilizing federal aid and informed them about the additional fees, but did not provide any advice or instructions. The counselor also encouraged the student to submit a FAFSA form, but this does not amount to an instructed check as it is a general recommendation and not a specific instruction. Therefore, the document is compliant with the instruction.",
            "item": "Transcript 3.pdf",
            "status": "passed"
          },
          {
            "excerpt": "['...we do have a scholarship right now for five beta Kappa. As long as you provide some kind of verification for it...', '...Were you thinking of potentially applying for financial aid to help with your investment?...']",
            "explanation": "The document failed to comply with the instructions. The counselor was found discussing financial aid options with the prospective student, which is against the instructions. The counselor mentioned a scholarship for five beta Kappa and asked the student if they were considering applying for financial aid. These instances indicate that the counselor was providing advice on financial aid, which is not allowed according to the instructions.",
            "item": "Transcript 1.pdf",
            "status": "failed"
          }
        ],
        "timestamp": "2024-06-25_14-57-21"
      },
      "status": "complete"
    },
    "status": "passed",
    "headers": ["item", "status", "explanation", "excerpt"]
  },
  "mode": "test_run"
}
```

## Error

For server-side errors, use this format to response

```json
{
  "error": {
    "code": 500,
    "message": "the executor server has error. details...",
    "details" "<debug info, only show in dev env>"
  }
}
```
