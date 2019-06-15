from time       import sleep
from unittest   import TestCase

from osbot_aws.apis.IAM                  import IAM
from osbot_aws.helpers.Create_Code_Build import Create_Code_Build
from pbx_gs_python_utils.utils.Assert    import Assert
from pbx_gs_python_utils.utils.Dev       import Dev

# NOTE at the moment the builds/osbot-jupyter/buildpsec.yml is done manually (need to write an api method to execute it)
# go to https://eu-west-2.console.aws.amazon.com/codesuite/codebuild/projects/gs-docker-codebuild/builds/start/advanced
# put 'builds/osbot-jupyter/buildpsec.yml' on the Buildspec -> 'Buildspec name - optional' textbox

class test_Create_Code_Build(TestCase):

    def setUp(self):
        self.project_name    = 'gs-docker-codebuild'
        self.profile_name    = 'gs-detect-aws'
        self.account_id      = IAM().account_id(self.profile_name)
        self.delete_project  = False
        self.api             = Create_Code_Build(account_id=self.account_id, project_name=self.project_name)

    # mising from this build workflow is the ECR create repository command (this was done manually)
    def test_create(self):
        if self.delete_project:
            self.api.delete_project_role_and_policies()
            assert self.api.code_build.project_exists()  is False
            assert self.api.code_build.iam.role_exists() is False

        expected_account_id     = '654386450934'
        expected_project_arn = 'arn:aws:codebuild:eu-west-2:{0}:project/{1}'.format(self.account_id, self.project_name)
        expected_build_id_start = 'arn:aws:codebuild:eu-west-2:654386450934:build/gs-docker-codebuild'.format(self.account_id, self.project_name)


        Assert(self.account_id      ).is_equal(expected_account_id                             )            # confirm account was correctly set from profile_name
        Assert(self.api.project_name).is_equal(self.project_name                               )            # confirm vars setup
        Assert(self.api.project_repo).is_equal('https://github.com/pbx-gs/' + self.project_name)            # confirm repo


        policies = self.api.policies__for_docker_build()
        self.api.create_role_and_policies(policies)
        sleep(1)                                                                                            # to give time for AWS to sync up internally

        assert self.api.create_project_with_container__docker()['project']['arn'] == expected_project_arn
        assert self.project_name                     in self.api.code_build.projects()                      # confirm project has been created
        assert self.api.code_build.iam.role_exists() is True                                                # confirm role has been created

        assert self.api.code_build.build_start().startswith(expected_build_id_start)                        # start build


    # use this to start a code build
    def test_build_start(self):
        build_id = self.api.code_build.build_start()
        result = self.api.code_build.build_wait_for_completion(build_id, max_attempts=100, log_status=True)
        Dev.pprint(result)



