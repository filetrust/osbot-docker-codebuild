from time import sleep

from pbx_gs_python_utils.utils.aws.CodeBuild import CodeBuild
from pbx_gs_python_utils.utils.aws.IAM import IAM


class Create_Code_Build:

    def __init__(self,project_name):
        self.account_id         = '244560807427'                                # move to config value or AWS Secret
        self.project_name       = project_name
        self.project_repo       = 'https://github.com/pbx-gs/{0}'.format(self.project_name)
        self.service_role       = 'arn:aws:iam::{0}:role/{1}'                  .format(self.account_id, self.project_name)
        self.project_arn        = 'arn:aws:codebuild:eu-west-2:{0}:project/{1}'.format(self.account_id, self.project_name     )
        self.assume_policy      = {'Statement': [{'Action'   : 'sts:AssumeRole'                     ,
                                                  'Effect'   : 'Allow'                              ,
                                                  'Principal': {'Service': 'codebuild.amazonaws.com'}}]}

        self.code_build = CodeBuild(role_name=self.project_name, project_name=self.project_name)
        self.iam        = IAM      (role_name=self.project_name                                )

    def setup(self,delete_on_setup=False):
        if delete_on_setup:
            self.code_build.project_delete()
            self.iam.role_delete()
        if self.code_build.project_exists() is False:
            assert self.code_build.project_exists() is False
            self.iam.role_create(self.assume_policy)                     # create role
            assert self.iam.role_info().get('Arn') == self.service_role  # confirm the role exists
            sleep(1)
            self.create_project()                                        # use this version

    def teardown(self, delete_on_teardown=False):

        assert self.code_build.project_exists() is True
        assert self.iam.role_exists() is True
        if delete_on_teardown:
            self.code_build.project_delete()
            self.iam.role_delete()
            assert self.code_build.project_exists() is False
            assert self.iam.role_exists() is False

    def create_project(self):
        kvargs = {
            'name'        : self.project_name,
            'source'      : { 'type'         : 'GITHUB',
                           'location'        : self.project_repo                 },
            'artifacts'   : {'type'          : 'NO_ARTIFACTS'                    },
            'environment' : {'type'          : 'LINUX_CONTAINER'                  ,
                            'image'          : 'aws/codebuild/docker:18.09.0'     ,
                            'computeType'    : 'BUILD_GENERAL1_LARGE'            },
                            #'privilegedMode' : True                              },
            'serviceRole' : self.service_role
        }

        return self.code_build.codebuild.create_project(**kvargs)

    def create_policies(self):
        cloud_watch_arn = "arn:aws:logs:eu-west-2:244560807427:log-group:/aws/codebuild/{0}:log-stream:*".format(self.project_name)
        policies = {"Cloud-Watch-Policy": { "Version": "2012-10-17",
                                            "Statement": [{   "Sid": "GsBotPolicy",
                                                              "Effect": "Allow",
                                                              "Action": [ "logs:CreateLogGroup"  ,
                                                                          "logs:CreateLogStream" ,
                                                                          "logs:PutLogEvents"   ],
                                                              "Resource": [ cloud_watch_arn ]}]},
                    "Secret-Manager": {
                                            "Version"  : "2012-10-17",
                                            "Statement": [{   "Sid"    : "GsBotPolicy",
                                                              "Effect" : "Allow",
                                                              "Action" : [ "secretsmanager:GetSecretValue","secretsmanager:DescribeSecret"],
                                                              "Resource": ["arn:aws:secretsmanager:eu-west-2:244560807427:secret:slack-gs-bot-*",
                                                                           "arn:aws:secretsmanager:eu-west-2:244560807427:secret:elastic_gsuite_data-*"]}]},
                    "Create-Docker-Image": {
                                            "Version"  : "2012-10-17",
                                            "Statement": [{     "Effect": "Allow"                            ,
                                                                "Action": [ "ecr:BatchCheckLayerAvailability",
                                                                            "ecr:CompleteLayerUpload"        ,
                                                                            "ecr:GetAuthorizationToken"      ,
                                                                            "ecr:InitiateLayerUpload"        ,
                                                                            "ecr:PutImage"                   ,
                                                                            "ecr:UploadLayerPart"]           ,
                                                                "Resource": "*"     }]}}

        policies_arns  = list(self.code_build.iam.role_policies().values())
        policies_names = list(self.code_build.iam.role_policies().keys())
        self.code_build.iam.role_policies_detach(policies_arns)
        for policies_name in policies_names:
            self.code_build.iam.policy_delete(policies_name)

        self.code_build.policies_create(policies)