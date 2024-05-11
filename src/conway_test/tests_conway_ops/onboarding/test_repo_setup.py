import sys                                                                          as _sys

from conway_acceptance.test_logic.acceptance_test_notes                             import AcceptanceTestNotes

from conway_ops.onboarding.repo_bundle                                              import RepoBundle
from conway_ops.onboarding.repo_setup                                               import RepoSetup

from conway_test.framework.test_logic.chassis_test_context                          import Chassis_TestContext
from conway_test.framework.test_logic.chassis_excels_to_compare                     import Chassis_ExcelsToCompare

from conway_test.tests_conway_ops.repo_manipulation_test_case                       import RepoManipulationTestCase

class TestRepoSetup(RepoManipulationTestCase):

    def test_repo_setup(self):
        '''
        Checks that the :class:`RepoAdministration` correctly creates a feature branch for all pertinent repos.

        '''
        MY_NAME                                         = "onboarding.test_repo_setup"

        notes                                           = AcceptanceTestNotes("database_structure", self.run_timestamp)

        excels_to_compare                               = Chassis_ExcelsToCompare()
        

        with Chassis_TestContext(MY_NAME, notes=notes) as ctx:

            project                                     = f"scratch_{ctx.scenario_id}"
            excels_to_compare.addXL_RepoStats(project)

            sdlc_root                                   = f"{ctx.manifest.path_to_seed()}/sdlc_root"

            local_repos_root                            = ctx.test_database.local_repos_hub.hub_root()
            remote_repos_root                           = ctx.test_database.remote_repos_hub.hub_root()

            # Pre-flight: create the repos in question
            self._create_github_repos(ctx)

            # Now we can do the test: setup local repos that are cloned from GitHub
            #
            admin                                       = RepoSetup(sdlc_root       = sdlc_root,
                                                                    profile_name    = self.profile_name)
            
            # Create the local development environment
            admin.setup(project)                

            admin.repo_bundle                           = RepoBundle(project)

            admin.create_repo_report(publications_folder=ctx.manifest.path_to_actuals(), mask_nondeterministic_data=True)

            self.assert_database_structure(ctx, excels_to_compare)  

if __name__ == "__main__":
    # In the debugger, executes only if we have a configuration that takes arguments, and the string
    # corresponding to the test method of interest should be configured in that configuration
    def main(args):
        T                                               = TestRepoSetup()
        T.setUp()
        what_to_do                                      = args[1]
        if what_to_do == "onboarding.test_repo_setup":
            T.test_repo_setup()

    main(_sys.argv)