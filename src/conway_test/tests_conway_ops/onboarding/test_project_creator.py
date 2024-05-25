import asyncio
import sys                                                                          as _sys

from conway_acceptance.test_logic.acceptance_test_notes                             import AcceptanceTestNotes

from conway_ops.onboarding.project_creator                                          import ProjectCreator

from conway_test.framework.test_logic.chassis_test_context                          import Chassis_TestContext
from conway_test.framework.test_logic.chassis_excels_to_compare                     import Chassis_ExcelsToCompare

from conway_test.tests_conway_ops.repo_manipulation_test_case                       import RepoManipulationTestCase

class TestProjectCreator(RepoManipulationTestCase):


    def test_create_minimalist_project(self):
        '''
        Checks that the :class:`ProjectCreator` correctly scaffolds a set of GIT repos for a standard
        project based on the :class:`conway`.

        '''
        MY_NAME                                         = "onboarding.test_create_minimalist_project"

        TEST_PROJECT                                    = "foo_app"

        notes                                           = AcceptanceTestNotes("database_structure", self.run_timestamp)

        excels_to_compare                               = Chassis_ExcelsToCompare()
        excels_to_compare.addXL_RepoStats(TEST_PROJECT)

        with Chassis_TestContext(MY_NAME, notes=notes) as ctx:

            local_repos_root                            = ctx.test_database.local_repos_hub.hub_root()
            remote_repos_root                           = ctx.test_database.remote_repos_hub.hub_root()

            admin                                       = ProjectCreator(   local_root             = local_repos_root, 
                                                                            remote_root            = remote_repos_root, 
                                                                            repo_bundle            = None,
                                                                            remote_gh_user         = None, 
                                                                            remote_gh_organization = None, 
                                                                            gh_secrets_path        = None)
            repo_bundle                                 = asyncio.run(admin.create_project(project_name     = TEST_PROJECT,
                                                                               work_branch_name = "bar-dev"))

            admin.repo_bundle                           = repo_bundle

            admin.create_repo_report(publications_folder=ctx.manifest.path_to_actuals(), mask_nondeterministic_data=True)

            self.assert_database_structure(ctx, excels_to_compare)       



if __name__ == "__main__":
    # In the debugger, executes only if we have a configuration that takes arguments, and the string
    # corresponding to the test method of interest should be configured in that configuration
    def main(args):
        T                                               = TestProjectCreator()
        T.setUp()
        what_to_do                                      = args[1]
        if what_to_do == "onboarding.test_create_minimalist_project":
            T.test_create_project()

    main(_sys.argv)