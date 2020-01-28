from time       import sleep
from unittest   import TestCase

from osbot_aws.apis.IAM                  import IAM
from osbot_aws.helpers.Create_Code_Build import Create_Code_Build
from pbx_gs_python_utils.utils.Assert    import Assert
from pbx_gs_python_utils.utils.Dev       import Dev

# NOTE at the moment the builds/osbot-jupyter/buildpsec.yml is done manually (need to write an api method to execute it)
# go to https://eu-west-2.console.aws.amazon.com/codesuite/codebuild/projects/gs-docker-codebuild/builds/start/advanced
# put 'builds/osbot-jupyter/buildspec.yml' on the Buildspec -> 'Buildspec name - optional' textbox
from gw_bot.helpers.Test_Helper import Test_Helper


class test_Create_Code_Build(Test_Helper):

    def setUp(self):
        super().setUp()
        self.github_org      = 'filetrust'
        self.source_version  = 'gw-bot-fork'
        self.project_name    = 'osbot-docker-codebuild'
        self.build_spec      = 'builds/osbot-jupyter/buildspec.yml'
        self.docker_type     = 'LINUX_CONTAINER'
        self.docker_image    = 'aws/codebuild/docker:18.09.0'
        self.compute_type    = 'BUILD_GENERAL1_LARGE'
        self.delete_project  = True
        self.api             = Create_Code_Build(project_name  =self.project_name  , github_org  =self.github_org  ,
                                                 source_version=self.source_version,
                                                 docker_type   =self.docker_type   , docker_image=self.docker_image,
                                                 compute_type  =self.compute_type  , build_spec  =self.build_spec  )
        self.account_id      = self.api.account_id
        self.region          = self.api.region

    def test_check_setup(self):
        assert self.api.account_id == "311800962295"
        assert self.api.region == 'eu-west-1'
        

    def test_create_all(self):
        if self.delete_project:
            self.api.delete_project_role_and_policies()
            assert self.api.code_build.project_exists()  is False
            assert self.api.code_build.iam.role_exists() is False

        expected_account_id     = '311800962295'
        expected_project_arn    = f'arn:aws:codebuild:{self.region}:{self.account_id}:project/{self.project_name}'
        expected_build_id_start = f'arn:aws:codebuild:{self.region}:{self.account_id}:build/{self.project_name}'


        Assert(self.account_id      ).is_equal(expected_account_id                             )            # confirm account was correctly set from profile_name
        Assert(self.api.project_name).is_equal(self.project_name                               )            # confirm vars setup
        Assert(self.api.project_repo).is_equal(f'https://github.com/{self.github_org}/{self.project_name}')            # confirm repo


        policies = self.api.policies__for_docker_build()
        self.api.create_role_and_policies(policies)
        sleep(1)                                                                                            # to give time for AWS to sync up internally
        # todo: figure out why the next line fails due to the AWS permission problem
        #       it is caused by some of IAM permissions not having been propagated
        assert self.api.create_project_with_container__docker()['project']['arn'] == expected_project_arn
        assert self.project_name                     in self.api.code_build.projects()                      # confirm project has been created
        assert self.api.code_build.iam.role_exists() is True                                                # confirm role has been created

        assert self.api.code_build.build_start().startswith(expected_build_id_start)                        # start build

    # run just this part independently (if it fails above)
    def test_just_create_project(self):
        expected_project_arn    = f'arn:aws:codebuild:{self.region}:{self.account_id}:project/{self.project_name}'
        expected_build_id_start = f'arn:aws:codebuild:{self.region}:{self.account_id}:build/{self.project_name}'

        assert self.api.create_project_with_container__docker()['project']['arn'] == expected_project_arn
        assert self.project_name                     in self.api.code_build.projects()                      # confirm project has been created
        assert self.api.code_build.iam.role_exists() is True                                                # confirm role has been created

        assert self.api.code_build.build_start().startswith(expected_build_id_start)                        # start build
    # use this to start a code build
    def test_build_start(self):
        build_id = self.api.code_build.build_start()
        result = self.api.code_build.build_wait_for_completion(build_id, max_attempts=100, log_status=True)
        Dev.pprint(result)



