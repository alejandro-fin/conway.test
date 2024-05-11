import abc

from conway.application.application                                 import Application

from conway_acceptance.test_logic.acceptance_test_case              import AcceptanceTestCase

from conway_ops.onboarding.user_profile                             import UserProfile
from conway_ops.repo_admin.github_repo_inspector                    import GitHub_RepoInspector



# GOTCHA
#
# Multiple inheritance is not ideal, and here we use it only in a "soft way". The "real parent class" for us is
# AcceptanceTestCase, and abc.ABC we only use as a way to tag some methods as abstract.
#
# Since Python does support multiple inheritance, this is allowed, but Python also has method resolution order (MRO)
# semantics whereby if there are multiple parent classes and a parent class's method is called, it will first try to
# match a method signature in the parent that was declared first (when reading left to right)
# 
# So it is essential that we put the AcceptanceTestCase parent *before* the abc.ABC parent in the declaration.
#
class RepoManipulationTestCase(AcceptanceTestCase, abc.ABC):
    '''
    This class serves as a parent class for test cases that create, modify, delete or examine GIT repos.

    It implements some useful methods that such tests cases usually need.
    '''

    def setUp(self):
        '''
        '''
        super().setUp()

        self.profile_name                           = "TestRobot@CCL"

    def _create_github_repos(self, ctx):
        '''
        Creates a collection of GitHub repos for the test case identified by `ctx.scenario_id`, 
        as per standard Conway semantics for projects.

        For example, if `ctx.scenario_id = 8002`, then under normal configuration this method would create
        these 5 repos in GitHub:

        * scenario_8002.docs, scenario_8002.ops, scenario_8002.scenarios, scenario_8002.svc, scenario_8002.test
        
        The configuration required to do this is taken from a user profile specific to the test case in question.
        That user profile defines things like:

        * GitHub account and credentials (expected to be set to a test account)
        * The repos to create for the project. In the above example, if `ctx.scenario_id = 8002`, then the project
          would be `scenario_8002` and the profile is expected to define what repos belong to that project.

        The user configuration is identified by the name `self.profile_name` and it must reside in the local 
        file system under a folder defined by `ctx.manifest.path_to_seed()`.

        :param Chassis_TestContext ctx: context manager controlling the environmental settings under which a particular
            test is running.

        :returns: the status from GitHub, as a JSON dictionary, on the attempt to create the GitRepo `repo_name`.
        :rtype: dict
        '''
        sdlc_root                                   = f"{ctx.manifest.path_to_seed()}/sdlc_root"
        profile_path                                = f"{sdlc_root}/sdlc.profiles/{self.profile_name}/profile.toml" 
        P                                           = UserProfile(profile_path)  

        project_name                                = f"scenario_{ctx.scenario_id}"  

        # Inspector object to connect to GitHub, but not tied to any specific repo
        github                                      = GitHub_RepoInspector(
                                                            parent_url          = P.REMOTE_ROOT,
                                                            repo_name           = None)

        pre_existing_repos                          = github.GET(resource_path = "/repos", resource = "orgs")
        pre_existing_repos                          = [] if pre_existing_repos is None else pre_existing_repos

        for repo_name in P.REPO_LIST(project_name):
             

            if repo_name in pre_existing_repos:
                raise ValueError(f"Can't create repo '{repo_name}' because it already exists in '{P.REMOTE_ROOT}'")

            # Create the repo
            #
            data_dict                               = github.POST(
                                                            resource_path   = "/repos",
                                                            resource        = "orgs",
                                                            body            = 
                                                                {"name":            repo_name,
                                                                "description":      "Repo used as a fixture by Conway tests"
                                                                })
            Application.app().log(f"Created repo '{repo_name}' - response was {data_dict}")

        

    def _get_files(self, root_folder):
        '''
        Overwrites parent to ignore files inside a ".git" folder, since GIT appears to use a non-deterministic
        way to hash objects

        @param root_folder A string representing the root of a folder structure
        '''
        all_files_l                                     = super()._get_files(root_folder)

        files_l                                         = [f for f in all_files_l if not ".git" in f.split("/")]

        return files_l