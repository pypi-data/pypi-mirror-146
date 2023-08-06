import pytest

from cx_releaser.src.release import Release


@pytest.mark.usefixtures("example_release_name")
@pytest.mark.usefixtures('example_aws_registry')
class TestReleasePush:

    @pytest.fixture(autouse=True)
    def get_release(self, example_aws_registry, example_release_name):
        self._release = Release.from_remote(example_release_name, example_aws_registry)

    def test_push(self):
        assert self._release.push() == '{Pushed Successfully}'

