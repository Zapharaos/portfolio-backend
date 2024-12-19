# portfolio-backend

[![codecov](https://codecov.io/gh/Zapharaos/portfolio-backend/graph/badge.svg?token=6T49GCFCLY)](https://codecov.io/gh/Zapharaos/portfolio-backend)

Repository related the backend of my own portfolio.

Link : www.matthieu-freitag.com/

## Table of Contents
- [Start the server](#start-the-server)
  - [Setup](#setup)
  - [Run the project](#run-the-project)
  - [Entrypoint error](#entrypoint-error)
  - [Create django superuser](#create-django-superuser)
  - [Access the admin panel](#access-the-admin-panel)
- [Customize your portfolio](#customize-your-portfolio)
  - [General](#general)
  - [About](#about)
  - [Experiences](#experiences)
  - [Files](#files)
  - [Footer](#footer)
  - [Hero](#hero)
  - [Projects](#projects)
  - [Socials](#socials)
  - [Technologies](#technologies)
  - [Users](#users)
  - [Work items](#work-items)
  - [Work](#work)

## Start the server

### Setup

Copy the `.env.dev` file into a new `.env` file and update the variables you want to change.<br>
If you are deploying for production, please copy `.env.prod.example` instead.

### Run the project

`docker-compose -f .\docker-compose.[environment].yml up`

Please replace `[environment]` by either `dev` or `prod`.

### Entrypoint error

```exec /usr/src/app/entrypoint.sh: no such file or directory```

You might run into the above error when starting the server.<br>
In that case, try replacing `#!/bin/sh` with `#!/bin/bash` inside `entrypoint.sh`.

### Create django superuser

`docker exec -it django python manage.py createsuperuser`

### Access the admin panel

Head to one of the below URL and login with the superuser you created.

- [http://localhost:8001/admin/](http://localhost:8001/admin/) for the development environment.
- [https://api.yourdomain.com.com/admin/](https://api.yourdomain.com/admin/) for the production environment.

## Customize your portfolio

Know that you've logged in to the admin panel, you can customize your portfolio by adding new projects, skills, etc.

### About

This table represents the about section of the portfolio.

| Fields          | Description                                                  |
|-----------------|--------------------------------------------------------------|
| Content type    | **Do not edit.** Defaults to `about`.                        |
| Image           | The main [File](#files) image used in the about section.     |
| ImageResponsive | An alternative [File](#files) image used on mobile versions. |
| Description     | Describe yourself.                                           |

### Experiences

This table represents the experiences section of the portfolio. These will be used to describe your work and academic
experiences.

| Fields       | Description                                                            |
|--------------|------------------------------------------------------------------------|
| Index        | The position or order of the experience in the list.                   |
| Hidden       | Boolean value indicating whether the experience is hidden.             |
| Title        | The title or role of the experience.                                   |
| Organisation | The name of the organization where the experience took place.          |
| Period       | The time period during which the experience occurred.                  |
| Location     | The location where the experience took place.                          |
| Url          | The URL to more information about the experience or organization.      |
| UrlShort     | A short URL or alias for the main URL.                                 |
| Description  | A detailed description of the experience.                              |
| Technologies | The [Technologies](#technologies) or tools used during the experience. |

### Files

This table represents the files uploaded to the portfolio. These will be used for images, resumes, etc.

| Fields          | Description                                   |
|-----------------|-----------------------------------------------|
| Name            | The name of the file.                         |
| File            | The actual file content or path to the file.  |
| CreditsUrl      | The URL to the credits or source of the file. |
| CreditsShortUrl | A short URL or alias for the credits URL.     |

Please note that `CreditsUrl` and `CreditsShortUrl` are only used by the [Hero](#hero) images (but are not required).

### Footer

This table represents the footer section of the portfolio.

| Fields       | Description                                                                          |
|--------------|--------------------------------------------------------------------------------------|
| Content type | **Do not edit.** Defaults to `footer`.                                               |
| Title        | The main heading or title displayed in the footer section.                           |
| SubTitle     | A short, catchy phrase or subtitle that complements the title.                       |
| ShowLocation | Boolean value indicating whether to display the [User](#users) location information. |
| ShowSocials  | Boolean value indicating whether to display the [Socials](#socials).                 |
| ShowEmail    | Boolean value indicating whether to display the [User](#users) email address.        |
| ShowResume   | Boolean value indicating whether to display a link to the [User](#users) resume.     |

### Hero

This table represents the hero section of the portfolio.

| Fields              | Description                                                         |
|---------------------|---------------------------------------------------------------------|
| Content type        | **Do not edit.** Defaults to `hero`.                                |
| Title               | The main heading or title displayed in the hero section.            |
| Tagline             | A short, catchy phrase or subtitle that complements the title.      |
| CallToActionContent | The text for the call-to-action button or link in the hero section. |
| BackgroundImage     | The [File](#files) image used in the hero section.                  |

### Projects

This table represents the projects section of the portfolio.

| Fields       | Description                                                         |
|--------------|---------------------------------------------------------------------|
| Index        | The position or order of the project in the list.                   |
| Hidden       | Boolean value indicating whether the project is hidden.             |
| Url          | The URL to more information about the project.                      |
| Title        | The title of the project.                                           |
| Description  | A detailed description of the project.                              |
| Image        | The [File](#files) image representing the project.                  |
| Technologies | The [Technologies](#technologies) or tools used during the project. |

### Socials

This table represents the [User](#users) social media links displayed in the footer section.

| Fields | Description                                                      |
|--------|------------------------------------------------------------------|
| IdUser | The unique identifier for the [User](#users).                    |
| Index  | The position or order of the social link in the list.            |
| Hidden | Boolean value indicating whether this social item is hidden.     |
| Name   | The name of the social media platform.                           |
| Pseudo | The username on the social media platform.                       |
| Url    | The URL to your social media profile.                            |
| Image  | The [File](#files) image representing the social media platform. |

### Technologies

This table represents the technologies or tools used in the portfolio.

| Fields | Description                 |
|--------|-----------------------------|
| Name   | The name of the technology. |

### Users

This table represents the user of the portfolio.

| Fields   | Description                                                     |
|----------|-----------------------------------------------------------------|
| Name     | The name of the user.                                           |
| Email    | The email address of the user.                                  |
| Location | The location of the user.                                       |
| Locale   | The locale or language preference of the user. Example: `fr-FR` |
| Logo     | The logo [File](#files) of the user.                            |
| Resume   | The resume or CV [File](#files) of the user.                    |
| Hero     | The [File](#hero) you want to display.                          |
| About    | The [About](#about) you want to display.                        |
| Work     | The [Work](#work) you want to display.                          |
| Footer   | The [Footer](#footer) you want to display.                      |

### Work items

This table represents the work items section of the portfolio.<br>
Please note that each `Work item` can contain [Projects](#projects) **or** [Experiences](#experiences), but never both.

For my own use case, I have created three of them : `Work`, `Projects` and `Education`.

| Fields          | Description                                                             |
|-----------------|-------------------------------------------------------------------------|
| Index           | The position or order of the work item in the list.                     |
| Hidden          | Boolean value indicating whether this work item is hidden.              |
| Title           | The title or name of the work item.                                     |
| Projects        | The [Projects](#projects) associated with this work item.               |
| Experiences     | The [Experiences](#experiences) associated with this work item.         |
| ShowProjects    | Boolean value indicating whether to display the associated projects.    |
| ShowExperiences | Boolean value indicating whether to display the associated experiences. |

### Work

This table represents the work section of the portfolio. This is where you select the [Work items](#work-items) you want
to display.

| Fields       | Description                                                              |
|--------------|--------------------------------------------------------------------------|
| Content type | **Do not edit.** Defaults to `work`.                                     |
| Items        | The list of [Work items](#work-items) associated with this work section. |