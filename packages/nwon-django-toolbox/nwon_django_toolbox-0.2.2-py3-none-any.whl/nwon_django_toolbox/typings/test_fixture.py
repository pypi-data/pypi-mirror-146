from nwon_baseline.typings import PydanticBaseDjango


class TestFixture(PydanticBaseDjango):
    path: str
    model_name: str
    preserve_password: bool
