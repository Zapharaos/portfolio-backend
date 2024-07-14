from user.models import File, Technology, Project, Experience, WorkItem, Work, Hero, About, Footer, User, Social


def create_sample_file(name="Name", creditsUrl="https://credits.com"):
    return File.objects.create(
        name=name, file="path/to/logo.png",
        creditsUrl=creditsUrl, creditsShortUrl="credits"
    )


def create_sample_technology(name="Name"):
    return Technology.objects.create(name=name)


def create_sample_project(title="Title"):
    project = Project.objects.create(
        index=1, hidden=False, url="https://project.com", title=title,
        description="A short description", image=create_sample_file()
    )
    project.technologies.set([create_sample_technology()])
    return project


def create_sample_experience(title="Title", url="https://experience.com"):
    experience = Experience.objects.create(
        index=1, hidden=False, title=title, organisation="Some Organization", period="2020-2022",
        location="fr-FR", url=url, urlShort="https://short.com", description="Description",
    )
    experience.technologies.set([create_sample_technology()])
    return experience


def create_sample_work_item(title="Title", showProjects=True, showExperiences=False):
    item = WorkItem.objects.create(
        index=1, hidden=False, title=title, showProjects=showProjects, showExperiences=showExperiences
    )
    item.projects.set([create_sample_project()])
    item.experiences.set([create_sample_experience()])
    return item


def create_sample_work(content_type="content_type"):
    work = Work.objects.create(content_type=content_type)
    work.items.set([create_sample_work_item()])
    return work


def create_sample_hero(content_type="content_type"):
    return Hero.objects.create(
        content_type=content_type, title="Hero", tagline="Tagline",
        callToActionContent="Click", backgroundImage=create_sample_file()
    )


def create_sample_about(content_type="content_type"):
    return About.objects.create(
        content_type=content_type, image=create_sample_file(),
        imageResponsive=create_sample_file(), description="Description"
    )


def create_sample_footer(content_type="content_type"):
    return Footer.objects.create(
        content_type=content_type, title="Sample Footer Title", subTitle="Sample Footer Subtitle",
        showLocation=True, showSocials=True, showEmail=True, showResume=True
    )


def create_sample_user():
    return User.objects.create(
        name="Test User", email="test@example.com", location="location", locale="locale",
        logo=create_sample_file(), resume=create_sample_file(),
        hero=create_sample_hero(), about=create_sample_about(),
        work=create_sample_work(), footer=create_sample_footer()
    )


def create_sample_social(name="Name"):
    return Social.objects.create(
        idUser=create_sample_user(), index=1, hidden=False,
        name=name, pseudo="Pseudo", url="https://social.com", image=create_sample_file()
    )
