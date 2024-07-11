from user.models import (
    File, Work, Hero, About, Footer, User
)


def create_sample_user():
    """
    Creates a sample user with pre-defined details and related objects.

    Returns:
        The newly created User object with related objects.
    """

    file = File.objects.create(name="Logo", file="path/to/logo.png")
    resume = File.objects.create(name="Resume", file="path/to/resume.pdf")
    hero = Hero.objects.create(title="Hero Title", tagline="Hero Tagline", callToActionContent="Click Here",
                               backgroundImage=file)
    about = About.objects.create(image=file, description="About description")
    work = Work.objects.create(content_type="work")
    footer = Footer.objects.create(title="Footer Title", subTitle="Footer SubTitle")

    user = User.objects.create(name="Test User", email="test@example.com", logo=file, resume=resume, hero=hero,
                               about=about, work=work, footer=footer)

    return user
