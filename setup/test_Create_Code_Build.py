import unittest
from time import sleep
from unittest import TestCase

from pbx_gs_python_utils.utils.Assert        import Assert
from pbx_gs_python_utils.utils.Dev import Dev

from setup.Create_Code_Build import Create_Code_Build


project_name = 'gs-docker-codebuild'

class test_Create_Code_Build(TestCase):

    @classmethod
    def setUpClass(cls):
        Create_Code_Build(project_name).setup(delete_on_setup=False)

    @classmethod
    def tearDownClass(cls):
        Create_Code_Build(project_name).teardown(delete_on_teardown = False)

    def setUp(self):
        self.api = Create_Code_Build(project_name)

    def test__init__(self):
        Assert(self.api.project_name).is_equal(project_name                               )      # confirm init vars setup
        Assert(self.api.project_repo).is_equal('https://github.com/pbx-gs/' + project_name)
        assert 'gsbot-gsuite' in self.api.code_build.projects()                                  # confirm project has been created
        assert self.api.iam.role_exists() is True                                                # confirm role has been created

    def test_create_policies(self):
        self.api.create_policies()

    def test_build_start(self):
        build_id = self.api.code_build.build_start()
        result = self.api.code_build.build_wait_for_completion(build_id, max_attempts=100, log_status=True)
        Dev.pprint(result)



